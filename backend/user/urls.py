from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"roles", RolViewSet, basename="role")
router.register(r"sector", SectorViewset, basename="sector")
router.register(r"admin", AdminUserCreateView, basename="admin")
router.register(r"reunions", ReunionViewSet, basename="reunion")
router.register(r"detalle_reuniones", DetalleReunionViewSet, basename="detalle_reunion")
router.register(r"invitados", InvitadoViewSet, basename="invitado")

urlpatterns = [
    path("", include(router.urls)),
]
