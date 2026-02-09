from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """ Проверка, является ли пользователь модератором. """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class IsNotModerator(BasePermission):
    """ Проверка, что пользователь НЕ является модератором. """
    def has_permission(self, request, view):
        return not request.user.groups.filter(name='moderators').exists()

class IsOwner(BasePermission):
    """ Проверка, является ли пользователь владельцем объекта. """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsOwnProfile(BasePermission):
    """ Проверка, что пользователь редактирует свой профиль. """
    def has_object_permission(self, request, view, obj):
        return obj == request.user
