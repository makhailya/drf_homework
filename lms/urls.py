from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonListCreateAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    # Course endpoints (через ViewSet и router)
    path('', include(router.urls)),

    # Lesson endpoints (через Generic-классы)
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
]
