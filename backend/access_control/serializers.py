from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, Rol, Permiso, Bitacora

class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = ['id', 'nombre', 'codigo', 'descripcion', 'activo', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']

class RolSerializer(serializers.ModelSerializer):
    permisos = PermisoSerializer(many=True, read_only=True)
    permisos_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion', 'permisos', 'permisos_ids', 'activo', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']

    def create(self, validated_data):
        permisos_ids = validated_data.pop('permisos_ids', [])
        rol = Rol.objects.create(**validated_data)
        
        if permisos_ids:
            permisos = Permiso.objects.filter(id__in=permisos_ids)
            rol.permisos.set(permisos)
        
        return rol

    def update(self, instance, validated_data):
        permisos_ids = validated_data.pop('permisos_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if permisos_ids is not None:
            permisos = Permiso.objects.filter(id__in=permisos_ids)
            instance.permisos.set(permisos)
        
        return instance

class UsuarioSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'password', 'telefono', 'direccion', 'rol', 'rol_nombre',
            'is_active', 'activo', 'date_joined', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'date_joined', 'fecha_actualizacion']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = Usuario.objects.create(**validated_data)
        
        if password:
            usuario.set_password(password)
            usuario.save()
        
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('Usuario inactivo')
            else:
                raise serializers.ValidationError('Credenciales inválidas')
        else:
            raise serializers.ValidationError('Debe proporcionar username y password')

        return data

class BitacoraSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Bitacora
        fields = ['id', 'usuario', 'usuario_nombre', 'accion', 'modelo_afectado', 
                 'id_objeto', 'descripcion', 'ip_address', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']