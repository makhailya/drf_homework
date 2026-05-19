from rest_framework import serializers
from .models import Course, Lesson
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """
    owner_email = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'preview', 'video_url', 'course', 'owner', 'owner_email')
        read_only_fields = ('owner',)
        extra_kwargs = {
            'video_url': {'validators': [validate_youtube_url]}
        }


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.
    Выводит количество уроков и список всех уроков курса.
    """
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
        'id', 'title', 'preview', 'description', 'lessons_count', 'lessons', 'owner', 'owner_email', 'is_subscribed')
        read_only_fields = ('owner',)

    def get_lessons_count(self, obj):
        """Получить количество уроков в курсе."""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверить, подписан ли текущий пользователь на курс."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.subscriptions.filter(user=request.user).exists()
        return False
