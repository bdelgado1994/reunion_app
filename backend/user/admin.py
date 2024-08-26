from django.contrib import admin
from .models import User, Rol, Sector, Reunion, DetalleReunion, Invitado

admin.site.register(Rol)
admin.site.register(User)
admin.site.register(Sector)
admin.site.register(Reunion)
admin.site.register(DetalleReunion)
admin.site.register(Invitado)
