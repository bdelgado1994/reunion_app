from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Rol, Sector, DetalleReunion, Reunion, Invitado
from django.contrib.auth import get_user_model
from .serializers import *
from .permissions import IsAdminOrSuperUserOrReadOnly

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUserOrReadOnly]


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUserOrReadOnly]


class AdminUserCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminCreationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUserOrReadOnly]

    def get_queryset(self):
        admin_role_name = "ADMIN"
        return User.objects.filter(roles__name=admin_role_name).distinct()


class SectorViewset(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [
        IsAdminOrSuperUserOrReadOnly,
    ]


class ReunionViewSet(viewsets.ModelViewSet):
    serializer_class = ReunionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUserOrReadOnly]

    def get_queryset(self):
        # Obtén el sector del usuario autenticado
        request = self.request
        if request and hasattr(request, "user"):
            sector = request.user.sector
            # Filtra las reuniones según el sector del usuario autenticado
            return Reunion.objects.filter(detalle_reunion__sector=sector)
        return (
            Reunion.objects.none()
        )  # Retorna un queryset vacío si no hay usuario autenticado


class DetalleReunionViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleReunionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUserOrReadOnly]

    def get_queryset(self):
        # Obtén el sector del usuario autenticado
        request = self.request
        if request and hasattr(request, "user"):
            sector = request.user.sector
            # Filtra los detalles de reuniones según el sector del usuario autenticado
            return DetalleReunion.objects.filter(sector=sector)
        return (
            DetalleReunion.objects.none()
        )  # Retorna un queryset vacío si no hay usuario autenticado


class InvitadoViewSet(viewsets.ModelViewSet):
    serializer_class = InvitadoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUserOrReadOnly]

    def get_queryset(self):
        # Obtén el sector del usuario autenticado
        request = self.request
        if request and hasattr(request, "user"):
            sector = request.user.sector
            # Filtra los invitados según el sector del usuario autenticado
            return Invitado.objects.filter(reunion__detalle_reunion__sector=sector)
        return (
            Invitado.objects.none()
        )  # Retorna un queryset vacío si no hay usuario autenticado

    def perform_create(self, serializer):
        request = self.request
        if request and hasattr(request, "user"):
            sector = request.user.sector
            reunion = serializer.validated_data.get("reunion")
            # Verifica si la reunión pertenece al sector del usuario autenticado
            if reunion and reunion.detalle_reunion.sector == sector:
                serializer.save()
            else:
                raise serializers.ValidationError(
                    "La reunión seleccionada no pertenece a su sector."
                )
        else:
            raise serializers.ValidationError(
                "Debe estar autenticado para crear un invitado."
            )
