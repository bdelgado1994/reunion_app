from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,AbstractBaseUser
from django.utils.translation import gettext_lazy as _

class Rol(models.Model):
    ADMIN="ADMIN"
    STAFF_USER="STAFF_USER"
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STAFF_USER, 'Staff User'),
    ]
    name=models.CharField(max_length=20,choices=ROLE_CHOICES,default=STAFF_USER)
    
    def __str__(self) -> str:
        return str(self.name).upper()

class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, password=None, **extra_fields):
        if username is None:
            raise ValueError(_('The Username field must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    roles = models.ManyToManyField(Rol, related_name="users", blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username or self.first_name
    
    def has_role(self, role_name):
        return self.roles.all().filter(name=role_name).exists()