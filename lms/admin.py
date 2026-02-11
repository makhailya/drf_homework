from django.contrib import admin
from .models import Course, Lesson, Subscription  # ← Добавили Subscription


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
    list_display = ('title', 'owner', 'get_lessons_count')
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
    list_display = ('title', 'course', 'owner', 'video_url')
    list_filter = ('course',)
    search_fields = ('title', 'description', 'course__title')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Админка для модели Subscription.
    """
    list_display = ('user', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('user__email', 'course__title')
