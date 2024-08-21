from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAdminOrSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # Permitir acceso de solo lectura (GET) a cualquier usuario, incluso si no están autenticados
            return True
        # Verificar si el usuario está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        # Permitir acceso completo (CRUD) solo a superusuarios o usuarios con rol 'ADMIN'
        return request.user.is_superuser or request.user.roles.filter(name='ADMIN').exists()