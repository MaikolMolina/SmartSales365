from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from ..models import Rol, Bitacora
from ..serializers import RolSerializer

class RolViewSet(viewsets.ModelViewSet):
    """
    CU14 - Gestionar Roles
    """
    queryset = Rol.objects.filter(activo=True)
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        rol = serializer.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='CREATE',
            modelo_afectado='Rol',
            id_objeto=rol.id,
            descripcion=f'Rol {rol.nombre} creado'
        )

    def perform_update(self, serializer):
        rol = serializer.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='UPDATE',
            modelo_afectado='Rol',
            id_objeto=rol.id,
            descripcion=f'Rol {rol.nombre} actualizado'
        )

    def perform_destroy(self, instance):
        # Soft delete
        instance.activo = False
        instance.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='DELETE',
            modelo_afectado='Rol',
            id_objeto=instance.id,
            descripcion=f'Rol {instance.nombre} desactivado'
        )