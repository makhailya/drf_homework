from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer, UserWithPaymentsSerializer
from .permissions import IsModerator, IsOwnProfile


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
            # Регистрация доступна всем
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Редактировать/удалять может только владелец профиля
            return [IsAuthenticated(), IsOwnProfile()]
        elif self.action == 'retrieve':
            # Просматривать свой профиль может любой авторизованный
            return [IsAuthenticated(), IsOwnProfile()]
        elif self.action == 'list':
            # Список пользователей только для модераторов
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
