# auth_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ..models import Bitacora

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
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
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
    return Response({'error': 'Usuario o contraseña incorrecta'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    Bitacora.objects.create(
        usuario=request.user,
        accion='LOGOUT',
        modelo_afectado='Usuario',
        id_objeto=request.user.id,
        descripcion='Cierre de sesión',
        ip_address=get_client_ip(request)
    )
    # No hace falta logout porque es stateless
    return Response({'message': 'Sesión cerrada exitosamente'})
