from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from users.models import User
from users.permissions import IsAdmin
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            return [IsAdmin()]
        return super().get_permissions()
    
    def perform_destroy(self, instance):        
        if instance.is_admin and not self.request.user.is_superuser:
            raise PermissionDenied("Un administrateur ne peut être supprimé que par un superutilisateur.")
        
        instance.delete()