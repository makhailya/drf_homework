from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'preview', 'video_url', 'course')


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.
    Выводит количество уроков и список всех уроков курса.
    """
    # Задание 1: Количество уроков
    lessons_count = serializers.SerializerMethodField()

    # Задание 3: Список уроков курса (вложенный сериализатор)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'lessons_count', 'lessons')

    def get_lessons_count(self, obj):
        """Получить количество уроков в курсе."""
        return obj.lessons.count()
