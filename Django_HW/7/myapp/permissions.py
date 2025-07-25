from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Кастомный пермишен, который разрешает только владельцам объекта редактировать его.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить чтение для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Запись разрешена только владельцу объекта
        return obj.owner == request.user
