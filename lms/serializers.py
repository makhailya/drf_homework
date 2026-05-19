from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """
    owner_email = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'preview', 'video_url', 'course', 'owner', 'owner_email')
        read_only_fields = ('owner',)


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.
    Выводит количество уроков и список всех уроков курса.
    """
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Course
        fields = (
        'id', 'title', 'preview', 'description', 'lessons_count', 'lessons', 'owner', 'owner_email')
        read_only_fields = ('owner',)

    def get_lessons_count(self, obj):
        """Получить количество уроков в курсе."""
        return obj.lessons.count()
