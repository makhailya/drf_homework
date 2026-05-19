from rest_framework.serializers import ValidationError
import re


class YouTubeURLValidator:
    """
    Валидатор для проверки, что URL ссылается только на YouTube.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        if url:
            # Проверяем, что ссылка содержит youtube.com
            if not re.search(r'(youtube\.com|youtu\.be)', url):
                raise ValidationError(
                    'Разрешены только ссылки на YouTube (youtube.com или youtu.be)'
                )


def validate_youtube_url(value):
    """
    Функция-валидатор для проверки YouTube ссылок.
    """
    if value:
        if not re.search(r'(youtube\.com|youtu\.be)', value):
            raise ValidationError(
                'Разрешены только ссылки на YouTube (youtube.com или youtu.be)'
            )
