from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели User.
    Предоставляет CRUD операции для пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    