from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Autorise uniquement les administrateurs."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_admin or request.user.is_superuser)
        )


class IsVeterinarian(BasePermission):
    """Autorise uniquement les vétérinaires."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_veterinarian or request.user.is_superuser)
        )


class IsSecretary(BasePermission):
    """Autorise uniquement les secrétaires."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_secretary or request.user.is_superuser)
        )