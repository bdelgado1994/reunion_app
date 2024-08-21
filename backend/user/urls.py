from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RolViewSet, AdminUserCreateView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RolViewSet, basename='role')
router.register(r'admin', AdminUserCreateView, basename='admin')

urlpatterns = [
    path('', include(router.urls)),
]