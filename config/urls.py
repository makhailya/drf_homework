"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Импортируем все ViewSet'ы
from users.views import UserViewSet, PaymentViewSet
from lms.views import CourseViewSet

# Создаём ОДИН главный роутер для всех ViewSet'ов
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Все ViewSet'ы через один роутер
    path('api/', include('lms.urls')),   # Только уроки (Generic views)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
