from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Rol

admin.site.register(Rol)

admin.site.register(User)
