from rest_framework import serializers
from .models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)
    course_title = serializers.CharField(source='paid_course.title', read_only=True)
    lesson_title = serializers.CharField(source='paid_lesson.title', read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id',
            'user',
            'user_email',
            'payment_date',
            'paid_course',
            'course_title',
            'paid_lesson',
            'lesson_title',
            'amount',
            'payment_method',
            'stripe_session_id',
            'payment_link',
            'payment_status',
        )
        read_only_fields = (
            'user',
            'payment_date',
            'stripe_session_id',
            'payment_link',
            'payment_status'
        )


# ← НОВЫЙ сериализатор с историей платежей
class UserWithPaymentsSerializer(serializers.ModelSerializer):
    """
    Расширенный сериализатор пользователя с историей платежей.
    """
    payments = PaymentSerializer(many=True, read_only=True)  # Вложенный сериализатор
    payments_count = serializers.SerializerMethodField()  # Количество платежей
    total_spent = serializers.SerializerMethodField()  # Общая сумма

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'city',
            'avatar',
            'date_joined',
            'payments_count',
            'total_spent',
            'payments'
        )
        read_only_fields = ('id', 'date_joined')

    def get_payments_count(self, obj):
        """Получить количество платежей пользователя."""
        return obj.payments.count()

    def get_total_spent(self, obj):
        """Получить общую сумму потраченных денег."""
        total = sum(payment.amount for payment in obj.payments.all())
        return float(total)


class UserSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для модели User (без платежей).
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'date_joined')
        read_only_fields = ('id', 'date_joined')
