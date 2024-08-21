from rest_framework import viewsets,generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Rol
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,RolSerializer,AdminCreationSerializer
from .permissions import IsAdminOrSuperUserOrReadOnly

User=get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes =[IsAdminOrSuperUserOrReadOnly]

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUserOrReadOnly]

class AdminUserCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminCreationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUserOrReadOnly]