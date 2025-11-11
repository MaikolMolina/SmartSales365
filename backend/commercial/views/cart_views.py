from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Sum, F
from ..models import CarritoCompra, Producto, Cliente
from ..serializers import (
    CarritoCompraSerializer, 
    AgregarAlCarritoSerializer,
    ActualizarCantidadSerializer
)
from backend.access_control.models import Bitacora

class CarritoCompraViewSet(viewsets.ModelViewSet):
    """
    CU18 - Gestionar Carrito de Compra
    """
    queryset = CarritoCompra.objects.all()
    serializer_class = CarritoCompraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Los clientes solo ven su propio carrito
        if self.request.user.rol and self.request.user.rol.nombre == 'Cliente':
            if hasattr(self.request.user, 'cliente') and self.request.user.cliente:
                return CarritoCompra.objects.filter(cliente=self.request.user.cliente)
            return CarritoCompra.objects.none()
        
        # Administradores ven todos los carritos
        return CarritoCompra.objects.all()

    def perform_create(self, serializer):
        # Asignar automáticamente el cliente del usuario autenticado
        if self.request.user.rol and self.request.user.rol.nombre == 'Cliente':
            if hasattr(self.request.user, 'cliente') and self.request.user.cliente:
                serializer.save(cliente=self.request.user.cliente)
            else:
                raise serializers.ValidationError('El usuario no tiene un cliente asociado.')
        else:
            # Si es administrador, debe especificar el cliente
            serializer.save()

    @action(detail=False, methods=['get'])
    def mi_carrito(self, request):
        """
        Endpoint para que los clientes vean su propio carrito
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
        
        carrito = CarritoCompra.objects.filter(cliente=request.user.cliente)
        serializer = self.get_serializer(carrito, many=True)
        
        # Calcular totales
        total_items = carrito.count()
        total_cantidad = carrito.aggregate(total=Sum('cantidad'))['total'] or 0
        total_precio = sum(item.subtotal for item in carrito)
        
        return Response({
            'items': serializer.data,
            'resumen': {
                'total_items': total_items,
                'total_cantidad': total_cantidad,
                'total_precio': total_precio
            }
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def agregar_producto(self, request):
        """
        Agregar producto al carrito
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
        
        serializer = AgregarAlCarritoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        producto_id = serializer.validated_data['producto_id']
        cantidad = serializer.validated_data['cantidad']
        
        try:
            producto = Producto.objects.get(id=producto_id, activo=True)
        except Producto.DoesNotExist:
            return Response(
                {'error': 'Producto no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Validar stock
        if cantidad > producto.stock:
            return Response(
                {'error': f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar si el producto ya está en el carrito
        carrito_item, created = CarritoCompra.objects.get_or_create(
            cliente=request.user.cliente,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        
        if not created:
            # Si ya existe, actualizar la cantidad
            nueva_cantidad = carrito_item.cantidad + cantidad
            if nueva_cantidad > producto.stock:
                return Response(
                    {'error': f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            carrito_item.cantidad = nueva_cantidad
            carrito_item.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=request.user,
            accion='CREATE',
            modelo_afectado='CarritoCompra',
            id_objeto=carrito_item.id,
            descripcion=f'Producto agregado al carrito: {producto.nombre}'
        )
        
        serializer_output = self.get_serializer(carrito_item)
        return Response({
            'message': 'Producto agregado al carrito',
            'item': serializer_output.data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def actualizar_cantidad(self, request, pk=None):
        """
        Actualizar cantidad de un item en el carrito
        """
        if not request.user.rol or request.user.rol.nombre != 'Cliente':
            return Response(
                {'error': 'Este endpoint es solo para clientes'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            carrito_item = CarritoCompra.objects.get(id=pk, cliente=request.user.cliente)
        except CarritoCompra.DoesNotExist:
            return Response(
                {'error': 'Item del carrito no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ActualizarCantidadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cantidad = serializer.validated_data['cantidad']
        
        # Validar stock
        if cantidad > carrito_item.producto.stock:
            return Response(
                {'error': f'Stock insuficiente. Solo hay {carrito_item.producto.stock} unidades disponibles.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        carrito_item.cantidad = cantidad
        carrito_item.save()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=request.user,
            accion='UPDATE',
            modelo_afectado='CarritoCompra',
            id_objeto=carrito_item.id,
            descripcion=f'Cantidad actualizada en carrito: {carrito_item.producto.nombre}'
        )
        
        serializer_output = self.get_serializer(carrito_item)
        return Response({
            'message': 'Cantidad actualizada',
            'item': serializer_output.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def vaciar_carrito(self, request):
        """
        Vaciar todo el carrito del cliente
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
        
        items_count = CarritoCompra.objects.filter(cliente=request.user.cliente).count()
        CarritoCompra.objects.filter(cliente=request.user.cliente).delete()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=request.user,
            accion='DELETE',
            modelo_afectado='CarritoCompra',
            descripcion=f'Carrito vaciado - {items_count} items eliminados'
        )
        
        return Response({
            'message': f'Carrito vaciado correctamente. Se eliminaron {items_count} items.'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def resumen(self, request):
        """
        Obtener resumen del carrito (total items, total precio)
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
        
        carrito = CarritoCompra.objects.filter(cliente=request.user.cliente)
        
        total_items = carrito.count()
        total_cantidad = carrito.aggregate(total=Sum('cantidad'))['total'] or 0
        total_precio = sum(item.subtotal for item in carrito)
        
        return Response({
            'total_items': total_items,
            'total_cantidad': total_cantidad,
            'total_precio': total_precio
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def finalizar_compra(self, request):
        """
        Finalizar compra - convertir carrito en ventas
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
        
        cliente = request.user.cliente
        carrito_items = CarritoCompra.objects.filter(cliente=cliente)
        
        if not carrito_items.exists():
            return Response(
                {'error': 'El carrito está vacío'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar stock antes de procesar
        for item in carrito_items:
            if item.cantidad > item.producto.stock:
                return Response(
                    {'error': f'Stock insuficiente para {item.producto.nombre}. Solo hay {item.producto.stock} unidades disponibles.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Crear ventas
        ventas_creadas = []
        total_compra = 0
        
        for item in carrito_items:
            # Crear venta
            venta = Venta.objects.create(
                cliente=cliente,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio,
                estado='COMPLETADA'
            )
            
            # Actualizar stock
            item.producto.stock -= item.cantidad
            item.producto.save()
            
            ventas_creadas.append({
                'id': venta.id,
                'producto': item.producto.nombre,
                'cantidad': item.cantidad,
                'total': venta.total
            })
            
            total_compra += venta.total
        
        # Vaciar carrito
        carrito_items.delete()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=request.user,
            accion='CREATE',
            modelo_afectado='Venta',
            descripcion=f'Compra finalizada - {len(ventas_creadas)} productos - Total: ${total_compra}'
        )
        
        return Response({
            'message': 'Compra finalizada exitosamente',
            'ventas_creadas': ventas_creadas,
            'total_compra': total_compra,
            'numero_ventas': len(ventas_creadas)
        }, status=status.HTTP_200_OK)