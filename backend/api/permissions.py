from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Кастомный класс ограничений, позволяющий отсеивать анонимных
    пользователей."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_staff
                         or request.user.is_superuser)))
