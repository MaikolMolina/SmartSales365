from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Usuario, Bitacora

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_fcm_token(request):
    """
    Endpoint para guardar/actualizar el token FCM del usuario
    """
    try:
        fcm_token = request.data.get('fcm_token')
        
        if not fcm_token:
            return Response(
                {'error': 'FCM token es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Actualizar token del usuario
        usuario = request.user
        usuario.fcm_token = fcm_token
        usuario.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=usuario,
            accion='UPDATE',
            modelo_afectado='Usuario',
            id_objeto=usuario.id,
            descripcion=f'Token FCM actualizado para {usuario.username}'
        )
        
        return Response({
            'message': 'Token FCM guardado exitosamente',
            'user': usuario.username
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error guardando token: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_fcm_token(request):
    """
    Endpoint para remover el token FCM (logout)
    """
    try:
        usuario = request.user
        usuario.fcm_token = None
        usuario.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=usuario,
            accion='UPDATE',
            modelo_afectado='Usuario',
            id_objeto=usuario.id,
            descripcion=f'Token FCM removido para {usuario.username}'
        )
        
        return Response({
            'message': 'Token FCM removido exitosamente'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error removiendo token: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )