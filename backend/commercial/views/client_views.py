from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Cliente
from ..serializers import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """
    Vista de clientes (solo para administradores)
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Los clientes solo pueden ver su propia información
        if self.request.user.rol and self.request.user.rol.nombre == 'Cliente':
            if hasattr(self.request.user, 'cliente') and self.request.user.cliente:
                return Cliente.objects.filter(id=self.request.user.cliente.id)
            return Cliente.objects.none()
        
        # Administradores ven todos los clientes
        return Cliente.objects.all()

    @action(detail=False, methods=['get'])
    def mi_perfil(self, request):
        """
        Endpoint para que los clientes vean su propio perfil
        """
        if not request.user.rol or request.user.rol.nombre != 'Cliente':
            return Response(
                {'error': 'Este endpoint es solo para clientes'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not hasattr(request.user, 'cliente') or not request.user.cliente:
            return Response(
                {'error': 'No se encontró información del cliente'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(request.user.cliente)
        return Response(serializer.data)