from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class Rol(models.Model):
    ADMIN = "ADMIN"
    STAFF_USER = "STAFF_USER"
    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (STAFF_USER, "Staff User"),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STAFF_USER)

    def __str__(self) -> str:
        return str(self.name).upper()


class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, password=None, **extra_fields):
        if username is None:
            raise ValueError(_("The Username field must be set"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class Sector(models.Model):
    name = models.CharField(max_length=150, null=False)

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        self.name = str(self.name).upper()
        return super(Sector, self).save(*args, **kwargs)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    roles = models.ManyToManyField(Rol, related_name="users", blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username or self.first_name

    def has_role(self, role_name):
        return self.roles.all().filter(name=role_name).exists()


class Reunion(models.Model):
    date = models.DateField()
    address = models.CharField(max_length=255)
    house_address = models.CharField(max_length=255)
    attendees_count = models.PositiveIntegerField()
    invited_count = models.PositiveIntegerField()
    offering_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reunión {self.id} - {self.date}"


class DetalleReunion(models.Model):
    reunion = models.OneToOneField(Reunion, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name="attended_reunions")
    sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, related_name="reuniones"
    )

    def __str__(self):
        return f"Detalle de Reunión {self.reunion.id}"

    def save(self, *args, **kwargs):
        if not self.reunion_id:
            latest_reunion = Reunion.objects.latest("id")
            self.reunion = latest_reunion
        return super(DetalleReunion, self).save(*args, **kwargs)


class Invitado(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    reunion = models.ForeignKey(
        Reunion, related_name="invitados", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Invitado {self.nombre} para la Reunión {self.reunion.id}"

    def save(self, *args, **kwargs):
        if not self.reunion_id:
            latest_reunion = Reunion.objects.latest("id")
            self.reunion = latest_reunion
        return super(Invitado, self).save(*args, **kwargs)
