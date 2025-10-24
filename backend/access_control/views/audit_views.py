from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Bitacora
from ..serializers import BitacoraSerializer

class BitacoraViewSet(viewsets.ReadOnlyModelViewSet):
    """
    CU15 - Gestionar Bitácora (solo lectura)
    """
    queryset = Bitacora.objects.all()
    serializer_class = BitacoraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Puedes agregar filtros aquí si es necesario
        return Bitacora.objects.all()