from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course


@shared_task
def send_course_update_notification(course_id):
    """
    Отправить уведомление подписчикам об обновлении курса.
    """
    try:
        course = Course.objects.get(id=course_id)

        # Получаем всех подписчиков курса
        subscriptions = course.subscriptions.select_related('user')

        if not subscriptions.exists():
            return f'Нет подписчиков для курса {course.title}'

        # Формируем список email
        subscriber_emails = [sub.user.email for sub in subscriptions]

        # Отправляем письма
        send_mail(
            subject=f'Обновление курса: {course.title}',
            message=f'Курс "{course.title}" был обновлён! Проверьте новые материалы.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=subscriber_emails,
            fail_silently=False,
        )

        return f'Уведомления отправлены {len(subscriber_emails)} подписчикам курса {course.title}'

    except Course.DoesNotExist:
        return f'Курс с ID {course_id} не найден'
    except Exception as e:
        return f'Ошибка отправки уведомлений: {str(e)}'
