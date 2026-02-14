from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .paginators import CoursePaginator, LessonPaginator
from .tasks import send_course_update_notification  # ← ДОБАВЬТЕ
from users.permissions import (
    IsModerator,
    IsOwner,
    IsNotModerator,
    IsModeratorOrOwner,
    IsOwnerAndNotModerator
)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.
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
            return [IsAuthenticated(), IsNotModerator()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsModeratorOrOwner()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsOwnerAndNotModerator()]
        elif self.action in ['retrieve', 'list']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Автоматически привязываем курс к создателю.
        """
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Обновление курса с отправкой уведомлений подписчикам.
        """
        course = self.get_object()

        # Проверяем, прошло ли более 4 часов с последнего обновления
        should_notify = True
        if course.updated_at:
            time_since_update = timezone.now() - course.updated_at
            if time_since_update < timedelta(hours=4):
                should_notify = False

        # Сохраняем изменения
        serializer.save()

        # Отправляем уведомления асинхронно (если прошло более 4 часов)
        if should_notify:
            send_course_update_notification.delay(course.id)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """
    Список уроков и создание нового урока.

    GET: Получить список всех уроков (модераторы видят все, пользователи - только свои)
    POST: Создать новый урок (только для не-модераторов)
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
            return [IsAuthenticated(), IsNotModerator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Автоматически привязываем урок к создателю.
        """
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Получить информацию о конкретном уроке.
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
    Обновить информацию об уроке (модераторы или владельцы).
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
    Удалить урок (только владельцы, не модераторы).
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

    POST: Подписаться или отписаться от курса (переключатель)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Подписаться или отписаться от курса.

        Параметры:
        - course_id: ID курса для подписки/отписки

        Возвращает:
        - message: "Подписка добавлена" или "Подписка удалена"
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
