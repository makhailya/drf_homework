from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .paginators import CoursePaginator, LessonPaginator
from users.permissions import (
    IsModerator,
    IsOwner,
    IsNotModerator,
    IsModeratorOrOwner,
    IsOwnerAndNotModerator
)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course с разграничением прав.
    """
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

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
            return [IsAuthenticated(), IsModeratorOrOwner()]
        elif self.action == 'destroy':
            # Удалять могут только владельцы (НЕ модераторы)
            return [IsAuthenticated(), IsOwnerAndNotModerator()]
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
    pagination_class = LessonPaginator

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
            return [IsAuthenticated(), IsNotModerator()]
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
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]

    def get_queryset(self):
        """
        Модераторы видят все уроки.
        Обычные пользователи видят только свои.
        """
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление урока.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerAndNotModerator]

    def get_queryset(self):
        """
        Только свои уроки (модераторы не видят чужие для удаления).
        """
        return Lesson.objects.filter(owner=self.request.user)


class SubscriptionAPIView(APIView):
    """
    Управление подпиской на курс.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Подписаться или отписаться от курса.
        """
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'error': 'course_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({'message': message}, status=status.HTTP_200_OK)
