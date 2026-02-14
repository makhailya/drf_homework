from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def deactivate_inactive_users():
    """
    Деактивировать пользователей, которые не заходили более месяца.
    """
    # Вычисляем дату месяц назад
    one_month_ago = timezone.now() - timedelta(days=30)

    # Находим активных пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=one_month_ago
    )

    # Считаем количество до блокировки
    count = inactive_users.count()

    # Блокируем пользователей
    inactive_users.update(is_active=False)

    return f'Заблокировано {count} неактивных пользователей'
