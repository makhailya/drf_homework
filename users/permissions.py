from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Проверка, является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(BasePermission):
    """
    Проверка, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnProfile(BasePermission):
    """
    Проверка, что пользователь редактирует свой профиль.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsNotModerator(BasePermission):
    """
    Проверка, что пользователь НЕ модератор.
    """

    def has_permission(self, request, view):
        return not request.user.groups.filter(name='moderators').exists()


class IsModeratorOrOwner(BasePermission):
    """
    Проверка, что пользователь - модератор ИЛИ владелец объекта.
    """

    def has_permission(self, request, view):
        # Модераторы проходят на уровне permission
        if request.user.groups.filter(name='moderators').exists():
            return True
        return True  # Для не-модераторов проверяем на уровне объекта

    def has_object_permission(self, request, view, obj):
        # Модераторы могут редактировать любые объекты
        if request.user.groups.filter(name='moderators').exists():
            return True
        # Обычные пользователи только свои
        return obj.owner == request.user


class IsOwnerAndNotModerator(BasePermission):
    """
    Проверка, что пользователь - владелец И НЕ модератор.
    """

    def has_permission(self, request, view):
        # Модераторы не проходят
        if request.user.groups.filter(name='moderators').exists():
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Проверяем, что НЕ модератор И владелец
        if request.user.groups.filter(name='moderators').exists():
            return False
        return obj.owner == request.user
