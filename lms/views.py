from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course.
    Предоставляет полный CRUD для курсов.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    Generic-класс для получения списка уроков и создания нового урока.
    GET: получить список всех уроков
    POST: создать новый урок
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Generic-класс для получения одного урока.
    GET: получить урок по ID
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Generic-класс для обновления урока.
    PUT/PATCH: обновить урок
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Generic-класс для удаления урока.
    DELETE: удалить урок
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    