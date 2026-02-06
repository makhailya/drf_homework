from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer, UserWithPaymentsSerializer
from .permissions import IsModerator


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
        if self.action == 'create':  # Регистрация доступна всем
            return [AllowAny()]
        return [IsAuthenticated()]  # Остальное только авторизованным

    def create(self, request, *args, **kwargs):
        """
        Регистрация нового пользователя.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Создаём пользователя с хешированным паролем
        user = User.objects.create_user(
            email=serializer.validated_data['email'],
            password=request.data.get('password'),
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
            phone=serializer.validated_data.get('phone', ''),
            city=serializer.validated_data.get('city', ''),
        )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Payment с фильтрацией и сортировкой.
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
