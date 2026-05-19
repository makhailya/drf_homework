from django.contrib import admin
from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    """
    Инлайн для отображения уроков в курсе.
    """
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Админка для модели Course.
    """
    list_display = ('title', 'get_lessons_count')
    search_fields = ('title', 'description')
    inlines = [LessonInline]

    def get_lessons_count(self, obj):
        """Получить количество уроков в курсе."""
        return obj.lessons.count()

    get_lessons_count.short_description = 'Количество уроков'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Админка для модели Lesson.
    """
    list_display = ('title', 'course', 'video_url')
    list_filter = ('course',)
    search_fields = ('title', 'description', 'course__title')
    