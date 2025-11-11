# auth_views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login
from backend.commercial.models import Cliente
from ..models import Bitacora, Usuario, Rol
from ..serializers import LoginSerializer, UsuarioSerializer

# Para tokens si usas DRF TokenAuthentication
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def register_client(request):
    """
    Registro público para clientes
    """
    try:
        data = request.data
        
        # Validar campos requeridos
        required_fields = ['username', 'email', 'password', 'nombre']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {'error': f'El campo {field} es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Verificar si el usuario ya existe
        if Usuario.objects.filter(username=data['username']).exists():
            return Response({'error': 'El nombre de usuario ya está en uso'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Usuario.objects.filter(email=data['email']).exists():
            return Response({'error': 'El email ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener o crear rol de Cliente
        rol_cliente, _ = Rol.objects.get_or_create(
            nombre='Cliente',
            defaults={'descripcion': 'Rol para clientes del sistema', 'activo': True}
        )
        
        # Crear cliente
        cliente = Cliente.objects.create(
            nombre=data['nombre'],
            email=data['email'],
            telefono=data.get('telefono', ''),
            direccion=data.get('direccion', '')
        )
        
        # Crear usuario
        usuario = Usuario.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            telefono=data.get('telefono', ''),
            direccion=data.get('direccion', ''),
            rol=rol_cliente,
            cliente=cliente
        )
        
        # Login automático
        login(request, usuario)
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=usuario,
            accion='CREATE',
            modelo_afectado='Usuario',
            id_objeto=usuario.id,
            descripcion=f'Cliente registrado: {usuario.username}',
            ip_address=get_client_ip(request)
        )
        
        return Response({
            'message': 'Registro exitoso',
            'user': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'rol': usuario.rol.nombre if usuario.rol else None,
                'cliente_id': cliente.id
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': f'Error en el registro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login simple sin authenticate
    """
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = Usuario.objects.get(username=username)
        if user.check_password(password):
            # Login y token
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)

            Bitacora.objects.create(
                usuario=user,
                accion='LOGIN',
                modelo_afectado='Usuario',
                id_objeto=user.id,
                descripcion='Inicio de sesión exitoso',
                ip_address=get_client_ip(request)
            )

            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'rol': user.rol.nombre if user.rol else None
                },
                'token': token.key
            })
        else:
            return Response({'error': 'Usuario o contraseña incorrecta'}, status=400)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario o contraseña incorrecta'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout simple (stateless)
    """
    Bitacora.objects.create(
        usuario=request.user,
        accion='LOGOUT',
        modelo_afectado='Usuario',
        id_objeto=request.user.id,
        descripcion='Cierre de sesión',
        ip_address=get_client_ip(request)
    )
    # No hace falta logout porque es stateless (token)
    return Response({'message': 'Sesión cerrada exitosamente'})
