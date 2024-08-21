from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.models import Rol,User


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rol
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'roles', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'roles']

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data.get('email', ''),
        )
        user.save()
        default_role, _ = Rol.objects.get_or_create(name="STAFF_USER")
        user.roles.add(default_role)
        return user

class AdminCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','first_name','last_name','email','password']
        read_only_fields =['id',]
        
    def validate(self, data):
        request = self.context.get("request")

        # Verificar si el usuario que realiza la solicitud tiene el rol de ADMIN
        if not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError("Debe estar autenticado para crear un usuario.")
        if not request.user.roles.filter(name="ADMIN").exists():
            raise serializers.ValidationError("Solo los usuarios con el rol de ADMIN pueden crear usuarios administradores.")
        
        # Verificar que los campos requeridos no estén vacíos
        if not data.get('username'):
            raise serializers.ValidationError("El campo 'username' es obligatorio.")
        if not data.get('password'):
            raise serializers.ValidationError("El campo 'password' es obligatorio.")
        
        # Verificar que el nombre de usuario sea único
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("El nombre de usuario ya está en uso.")
        
        return data

    def create(self, validated_data):
        # Crear el usuario
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        # Asignar el rol ADMIN al usuario recién creado
        admin_role, _ = Rol.objects.get_or_create(name="ADMIN")
        user.roles.add(admin_role)
        return user