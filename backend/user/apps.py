from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.utils import OperationalError


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        post_migrate.connect(create_default_sector_and_roles, sender=self)


def create_default_sector_and_roles(sender, **kwargs):
    from .models import Rol, Sector  # Importa los modelos dentro de la función

    try:
        # Intenta obtener el sector con ID 1
        try:
            sector = Sector.objects.get(pk=1)
        except Sector.DoesNotExist:
            # Si el sector no existe, créalo con el nombre "N/A"
            sector = Sector.objects.create(name="N/A")
            if sector:
                print(f'Sector "{sector.name}" creado.')

        roles_to_create = [
            {"name": Rol.ADMIN},
            {"name": Rol.STAFF_USER},
        ]

        for role_data in roles_to_create:
            # Crea el rol si no existe
            role, created = Rol.objects.get_or_create(name=role_data["name"])
            if created:
                print(f'Rol "{role.name}" creado.')

    except OperationalError:
        # Si ocurre un error de la base de datos, significa que las tablas aún no existen
        print("Las tablas aún no existen. Saltando la creación de sectores y roles.")
