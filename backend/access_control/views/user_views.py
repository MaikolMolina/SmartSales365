from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Usuario, Bitacora
from ..serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    CU13 - Gestionar Usuario
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Solo usuarios activos
        return Usuario.objects.filter(activo=True)

    def perform_create(self, serializer):
        usuario = serializer.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='CREATE',
            modelo_afectado='Usuario',
            id_objeto=usuario.id,
            descripcion=f'Usuario {usuario.username} creado'
        )

    def perform_update(self, serializer):
        usuario = serializer.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='UPDATE',
            modelo_afectado='Usuario',
            id_objeto=usuario.id,
            descripcion=f'Usuario {usuario.username} actualizado'
        )

    def perform_destroy(self, instance):
        # Soft delete - marcar como inactivo en lugar de eliminar
        instance.activo = False
        instance.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='DELETE',
            modelo_afectado='Usuario',
            id_objeto=instance.id,
            descripcion=f'Usuario {instance.username} desactivado'
        )

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Obtener información del usuario actual
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)