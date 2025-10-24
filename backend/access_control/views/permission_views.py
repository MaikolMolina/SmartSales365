from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from ..models import Permiso, Bitacora
from ..serializers import PermisoSerializer

class PermisoViewSet(viewsets.ModelViewSet):
    """
    CU22 - Gestionar Permisos
    """
    queryset = Permiso.objects.filter(activo=True)
    serializer_class = PermisoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        permiso = serializer.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='CREATE',
            modelo_afectado='Permiso',
            id_objeto=permiso.id,
            descripcion=f'Permiso {permiso.nombre} creado'
        )

    def perform_update(self, serializer):
        permiso = serializer.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='UPDATE',
            modelo_afectado='Permiso',
            id_objeto=permiso.id,
            descripcion=f'Permiso {permiso.nombre} actualizado'
        )

    def perform_destroy(self, instance):
        # Soft delete
        instance.activo = False
        instance.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='DELETE',
            modelo_afectado='Permiso',
            id_objeto=instance.id,
            descripcion=f'Permiso {instance.nombre} desactivado'
        )