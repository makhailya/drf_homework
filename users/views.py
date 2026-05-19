from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer, UserWithPaymentsSerializer
from .permissions import IsModerator, IsOwnProfile
from .services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
    retrieve_stripe_session,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели User с регистрацией.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """
        Использовать расширенный сериализатор для retrieve.
        """
        if self.action == 'retrieve':
            return UserWithPaymentsSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Разные права для разных действий.
        """
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnProfile()]
        elif self.action == 'retrieve':
            return [IsAuthenticated(), IsOwnProfile()]
        elif self.action == 'list':
            return [IsAuthenticated(), IsModerator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Регистрация нового пользователя с хешированием пароля.
        """
        password = self.request.data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()

    def perform_update(self, serializer):
        """
        Обновление пользователя с хешированием пароля (если передан).
        """
        password = self.request.data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Payment с фильтрацией, сортировкой и Stripe интеграцией.
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']

    def get_queryset(self):
        """
        Модераторы видят все платежи.
        Обычные пользователи видят только свои.
        """
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Payment.objects.all()
        return Payment.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        """
        Создать платёж с интеграцией Stripe.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Создаём платёж
        payment = serializer.save(user=request.user)

        # Определяем название продукта
        if payment.paid_course:
            product_name = payment.paid_course.title
        elif payment.paid_lesson:
            product_name = payment.paid_lesson.title
        else:
            product_name = "Продукт"

        try:
            # Создаём продукт в Stripe
            stripe_product = create_stripe_product(product_name)

            # Создаём цену в Stripe
            stripe_price = create_stripe_price(stripe_product.id, payment.amount)

            # Создаём сессию оплаты
            stripe_session = create_stripe_session(stripe_price.id)

            # Сохраняем данные Stripe в платеже
            payment.stripe_session_id = stripe_session.id
            payment.payment_link = stripe_session.url
            payment.save()

            # Возвращаем данные с ссылкой на оплату
            return Response({
                'id': payment.id,
                'amount': payment.amount,
                'payment_link': payment.payment_link,
                'session_id': payment.stripe_session_id,
                'status': payment.payment_status,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Если ошибка - удаляем созданный платёж
            payment.delete()
            return Response(
                {'error': f'Ошибка создания платежа: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Проверить статус платежа в Stripe.
        """
        payment = self.get_object()

        if not payment.stripe_session_id:
            return Response(
                {'error': 'Платёж не связан с Stripe'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Получаем данные из Stripe
            session = retrieve_stripe_session(payment.stripe_session_id)

            # Обновляем статус платежа
            if session.payment_status == 'paid':
                payment.payment_status = 'paid'
            elif session.payment_status == 'unpaid':
                payment.payment_status = 'pending'
            else:
                payment.payment_status = 'failed'

            payment.save()

            return Response({
                'payment_id': payment.id,
                'stripe_status': session.payment_status,
                'status': payment.payment_status,
                'amount': payment.amount,
            })

        except Exception as e:
            return Response(
                {'error': f'Ошибка получения статуса: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
