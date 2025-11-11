from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Producto
from ..serializers import ProductoSerializer

class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista de productos (solo lectura para clientes)
    """
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrar productos activos y con stock
        return Producto.objects.filter(activo=True, stock__gt=0)