from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from ..models import Venta, Producto, Cliente
from ..serializers import VentaSerializer
from backend.access_control.models import Bitacora

class VentaViewSet(viewsets.ModelViewSet):
    """
    CU05 - Registrar Venta
    """
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Los clientes solo ven sus propias ventas
        if self.request.user.rol and self.request.user.rol.nombre == 'Cliente':
            if hasattr(self.request.user, 'cliente') and self.request.user.cliente:
                return Venta.objects.filter(cliente=self.request.user.cliente)
            return Venta.objects.none()
        
        # Administradores ven todas las ventas
        return Venta.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        # Validar stock antes de crear la venta
        producto = serializer.validated_data['producto']
        cantidad = serializer.validated_data['cantidad']
        
        if cantidad > producto.stock:
            raise serializers.ValidationError(
                f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.'
            )
        
        # Crear la venta
        venta = serializer.save()
        
        # Actualizar stock del producto
        producto.stock -= cantidad
        producto.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='CREATE',
            modelo_afectado='Venta',
            id_objeto=venta.id,
            descripcion=f'Venta registrada - Producto: {producto.nombre}, Cantidad: {cantidad}'
        )

    def perform_update(self, serializer):
        venta = serializer.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='UPDATE',
            modelo_afectado='Venta',
            id_objeto=venta.id,
            descripcion=f'Venta actualizada - ID: {venta.id}'
        )

    def perform_destroy(self, instance):
        # Restaurar stock al eliminar venta
        producto = instance.producto
        producto.stock += instance.cantidad
        producto.save()
        
        # Registrar en bitácora antes de eliminar
        Bitacora.objects.create(
            usuario=self.request.user,
            accion='DELETE',
            modelo_afectado='Venta',
            id_objeto=instance.id,
            descripcion=f'Venta eliminada - Producto: {instance.producto.nombre}'
        )
        
        instance.delete()

    @action(detail=False, methods=['get'])
    def mis_ventas(self, request):
        """
        Endpoint para que los clientes vean sus propias ventas
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
        
        ventas = Venta.objects.filter(cliente=request.user.cliente).order_by('-fecha_venta')
        serializer = self.get_serializer(ventas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Estadísticas de ventas (solo para administradores)
        """
        if not request.user.rol or request.user.rol.nombre != 'Administrador':
            return Response(
                {'error': 'Solo los administradores pueden ver estadísticas'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        from django.db.models import Sum, Count, Avg
        from datetime import datetime, timedelta
        
        # Ventas del último mes
        ultimo_mes = datetime.now() - timedelta(days=30)
        ventas_ultimo_mes = Venta.objects.filter(fecha_venta__gte=ultimo_mes)
        
        estadisticas = {
            'total_ventas': Venta.objects.count(),
            'ventas_ultimo_mes': ventas_ultimo_mes.count(),
            'ingresos_totales': Venta.objects.aggregate(Sum('total'))['total__sum'] or 0,
            'ingresos_ultimo_mes': ventas_ultimo_mes.aggregate(Sum('total'))['total__sum'] or 0,
            'producto_mas_vendido': Venta.objects.values('producto__nombre')
                .annotate(total=Sum('cantidad'))
                .order_by('-total')
                .first(),
            'promedio_venta': Venta.objects.aggregate(Avg('total'))['total__avg'] or 0,
        }
        
        return Response(estadisticas)