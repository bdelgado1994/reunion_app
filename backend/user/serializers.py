from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.models import *


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.StringRelatedField(many=True, read_only=True)
    sector = serializers.PrimaryKeyRelatedField(
        queryset=Sector.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = ["id", "roles", "first_name", "last_name", "email", "sector"]
        read_only_fields = ["id", "roles"]

    def create(self, validated_data):
        sector = validated_data.get("sector", Sector.objects.get(pk=1))
        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data.get("email", ""),
            sector=sector,
        )
        user.save()
        default_role, _ = Rol.objects.get_or_create(name="STAFF_USER")
        user.roles.add(default_role)
        return user


class AdminCreationSerializer(serializers.ModelSerializer):
    sector = serializers.PrimaryKeyRelatedField(
        queryset=Sector.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "sector",
        ]
        read_only_fields = [
            "id",
        ]

    def validate(self, data):
        request = self.context.get("request")

        # Verificar si el usuario que realiza la solicitud está autenticado
        if not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Debe estar autenticado para crear un usuario."
            )

        # Verificar si el usuario autenticado tiene el rol de ADMIN o es superusuario
        if (
            not request.user.roles.filter(name="ADMIN").exists()
            and not request.user.is_superuser
        ):
            raise serializers.ValidationError(
                "Solo los usuarios con el rol de ADMIN o los superusuarios pueden crear usuarios administradores."
            )

        # Verificar que los campos requeridos no estén vacíos
        if not data.get("username"):
            raise serializers.ValidationError("El campo 'username' es obligatorio.")
        if not data.get("password"):
            raise serializers.ValidationError("El campo 'password' es obligatorio.")

        # Verificar que el nombre de usuario sea único
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("El nombre de usuario ya está en uso.")

        return data

    def create(self, validated_data):
        sector = validated_data.get("sector", Sector.objects.get(pk=1))
        # Crear el usuario
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            sector=sector,
        )
        user.set_password(validated_data["password"])
        user.save()
        # Asignar el rol ADMIN al usuario recién creado
        admin_role, _ = Rol.objects.get_or_create(name="ADMIN")
        user.roles.add(admin_role)
        return user

    def update(self, instance, validated_data):
        # Actualizar los campos del usuario
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.sector = validated_data.get("sector", instance.sector)

        # Actualizar la contraseña si se proporciona
        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"


class ReunionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reunion
        fields = "__all__"


class DetalleReunionSerializer(serializers.ModelSerializer):
    reunion = serializers.PrimaryKeyRelatedField(queryset=Reunion.objects.all())
    attendees = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(), many=True
    )
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())

    class Meta:
        model = DetalleReunion
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(DetalleReunionSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            # Filtrar los usuarios (asistentes) según el sector del usuario autenticado
            self.fields["attendees"].queryset = User.objects.filter(
                sector=request.user.sector
            )
            # Filtrar los sectores disponibles en caso de que se quiera asignar un sector
            self.fields["sector"].queryset = Sector.objects.filter(
                id=request.user.sector.id
            )


class InvitadoSerializer(serializers.ModelSerializer):
    reunion = serializers.PrimaryKeyRelatedField(queryset=Reunion.objects.all())

    class Meta:
        model = Invitado
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(InvitadoSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            # Filtrar las reuniones disponibles según el sector del usuario autenticado
            self.fields["reunion"].queryset = Reunion.objects.filter(
                detalle_reunion__sector=request.user.sector
            )
