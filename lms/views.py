from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner, IsNotModerator


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course с разграничением прав.
    """
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Модераторы видят все курсы.
        Обычные пользователи видят только свои.
        """
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        """
        Разные права для разных действий.
        """
        if self.action == 'create':
            # Создавать могут только НЕ модераторы
            return [IsAuthenticated(), IsNotModerator()]
        elif self.action in ['update', 'partial_update']:
            # Редактировать могут модераторы ИЛИ владельцы
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        elif self.action == 'destroy':
            # Удалять могут только владельцы (НЕ модераторы)
            return [IsAuthenticated(), IsOwner(), IsNotModerator()]
        elif self.action in ['retrieve', 'list']:
            # Просматривать могут все авторизованные
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Автоматически привязываем курс к создателю.
        """
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    Список и создание уроков.
    """
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Модераторы видят все уроки.
        Обычные пользователи видят только свои.
        """
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        """
        Права доступа.
        """
        if self.request.method == 'POST':
            # Создавать могут только НЕ модераторы
            return [IsAuthenticated(), ~IsModerator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Автоматически привязываем урок к создателю.
        """
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Просмотр одного урока.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Модераторы видят все уроки.
        Обычные пользователи видят только свои.
        """
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Обновление урока.
    """
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Модераторы видят все уроки.
        Обычные пользователи видят только свои.
        """
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        """
        Редактировать могут модераторы ИЛИ владельцы.
        """
        return [IsAuthenticated(), IsModerator() | IsOwner()]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление урока.
    """
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Только свои уроки (модераторы не видят чужие для удаления).
        """
        return Lesson.objects.filter(owner=self.request.user)

    def get_permissions(self):
        """
        Удалять могут только владельцы (НЕ модераторы).
        """
        return [IsAuthenticated(), IsOwner(), ~IsModerator()]
