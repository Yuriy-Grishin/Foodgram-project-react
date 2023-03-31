from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Автору доступны все виды запросов, в том числе запись и удаление, а остальным доступны только безопасные запросы (чтение)"""

    """Общая  проверка разрешения для всех запросов"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated or request.method in permissions.SAFE_METHODS
        )

    """Проверка для конкретного экземпляра объекта"""

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user
