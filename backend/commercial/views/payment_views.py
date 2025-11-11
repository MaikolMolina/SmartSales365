from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from ..models import Pago, OrdenCompra, Cliente, Venta, CarritoCompra
from ..serializers import PagoSerializer, OrdenCompraSerializer, CrearSesionPagoSerializer
from ..services.stripe_service import StripeService
from backend.access_control.models import Bitacora

class PagoViewSet(viewsets.ModelViewSet):
    """
    Vista para gestionar pagos
    """
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Los clientes solo ven sus propios pagos
        if self.request.user.rol and self.request.user.rol.nombre == 'Cliente':
            if hasattr(self.request.user, 'cliente') and self.request.user.cliente:
                return Pago.objects.filter(cliente=self.request.user.cliente)
            return Pago.objects.none()
        
        # Administradores ven todos los pagos
        return Pago.objects.all()

    @action(detail=False, methods=['post'])
    def crear_sesion_pago(self, request):
        """
        Crea una sesión de pago de Stripe para una orden existente o un monto específico
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
        
        serializer = CrearSesionPagoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        cliente = request.user.cliente
        
        try:
            with transaction.atomic():
                if 'orden_id' in data:
                    # Pago para una orden existente
                    orden = get_object_or_404(OrdenCompra, id=data['orden_id'], cliente=cliente)
                    monto = orden.total
                    descripcion = f"Orden #{orden.id}"
                    metadata = {'orden_id': str(orden.id)}
                    
                else:
                    # Pago directo (sin orden)
                    monto = data['monto']
                    descripcion = data.get('descripcion', 'Pago SmartSales365')
                    metadata = {'tipo': 'pago_directo'}
                    
                    # Crear orden temporal
                    orden = OrdenCompra.objects.create(
                        cliente=cliente,
                        items=[],  # Items vacíos para pagos directos
                        total=monto,
                        estado='PENDIENTE'
                    )
                    metadata['orden_id'] = str(orden.id)
                
                # URLs de redirección
                success_url = f"{settings.PAYMENT_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}"
                cancel_url = settings.PAYMENT_CANCEL_URL
                
                # Crear sesión de Stripe
                if 'orden_id' in data and data['orden_id']:
                    checkout_session = StripeService.crear_sesion_pago(
                        orden, success_url, cancel_url, metadata
                    )
                else:
                    checkout_session = StripeService.crear_sesion_pago_simple(
                        monto, descripcion, success_url, cancel_url, metadata
                    )
                
                # Crear registro de pago
                pago = Pago.objects.create(
                    cliente=cliente,
                    orden=orden if 'orden_id' not in data else None,
                    metodo_pago='STRIPE',
                    monto=monto,
                    estado='PENDIENTE',
                    stripe_checkout_session_id=checkout_session.id,
                    descripcion=descripcion,
                    metadata=metadata
                )
                
                # Actualizar orden con el pago
                if 'orden_id' not in data:
                    orden.pago = pago
                    orden.save()
                
                # Registrar en bitácora
                Bitacora.objects.create(
                    usuario=request.user,
                    accion='CREATE',
                    modelo_afectado='Pago',
                    id_objeto=pago.id,
                    descripcion=f'Sesión de pago creada - ${monto}'
                )
                
                return Response({
                    'session_id': checkout_session.id,
                    'url_pago': checkout_session.url,
                    'pago_id': pago.id,
                    'orden_id': orden.id
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {'error': f'Error creando sesión de pago: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @action(detail=False, methods=['post'])
    def pago_desde_carrito(self, request):
        """
        Crea una orden y sesión de pago desde el carrito del cliente
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
        
        try:
            with transaction.atomic():
                # Obtener items del carrito
                carrito_items = CarritoCompra.objects.filter(cliente=cliente)
                
                if not carrito_items.exists():
                    return Response(
                        {'error': 'El carrito está vacío'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Preparar items para la orden
                items_orden = []
                total = 0
                
                for item in carrito_items:
                    item_data = {
                        'producto_id': item.producto.id,
                        'producto_nombre': item.producto.nombre,
                        # Usar descripción no vacía para Stripe
                        'descripcion': item.producto.descripcion or 'Producto sin descripción',
                        'cantidad': item.cantidad,
                        'precio': float(item.producto.precio),
                        'subtotal': float(item.subtotal)
                    }
                    items_orden.append(item_data)
                    total += item.subtotal
                
                # Crear orden de compra
                orden = OrdenCompra.objects.create(
                    cliente=cliente,
                    items=items_orden,
                    total=total,
                    estado='PENDIENTE'
                )
                
                # Crear sesión de pago
                success_url = f"{settings.PAYMENT_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}&orden_id={orden.id}"
                cancel_url = settings.PAYMENT_CANCEL_URL
                
                checkout_session = StripeService.crear_sesion_pago(
                    orden_compra=orden,
                    success_url=success_url,
                    cancel_url=cancel_url,
                    metadata={'orden_id': str(orden.id)}
                )
                
                # Crear registro de pago (sin orden=)
                pago = Pago.objects.create(
                    cliente=cliente,
                    metodo_pago='STRIPE',
                    monto=total,
                    estado='PENDIENTE',
                    stripe_checkout_session_id=checkout_session.id,
                    descripcion=f"Orden #{orden.id} - Carrito de compras",
                    metadata={'orden_id': str(orden.id), 'tipo': 'carrito'}
                )
                
                # Asignar pago a la orden
                orden.pago = pago
                orden.save()
                
                # Registrar en bitácora
                Bitacora.objects.create(
                    usuario=request.user,
                    accion='CREATE',
                    modelo_afectado='Pago',
                    id_objeto=pago.id,
                    descripcion=f'Pago desde carrito creado - ${total}'
                )
                
                return Response({
                    'session_id': checkout_session.id,
                    'url_pago': checkout_session.url,
                    'pago_id': pago.id,
                    'orden_id': orden.id,
                    'total': total
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {'error': f'Error procesando pago desde carrito: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def verificar_estado(self, request, pk=None):
        """
        Verifica el estado actual de un pago
        """
        pago = self.get_object()
        
        try:
            if pago.stripe_checkout_session_id:
                session = StripeService.obtener_sesion(pago.stripe_checkout_session_id)
                
                if session.payment_status == 'paid':
                    pago.marcar_como_completado()
                    # Aquí podrías triggerear otras acciones (enviar email, etc.)
                
                return Response({
                    'pago_id': pago.id,
                    'estado_stripe': session.payment_status,
                    'estado_local': pago.estado,
                    'session': {
                        'id': session.id,
                        'payment_intent': session.payment_intent,
                        'amount_total': session.amount_total / 100,  # Convertir de centavos
                        'currency': session.currency
                    }
                })
            else:
                return Response({
                    'pago_id': pago.id,
                    'estado_local': pago.estado,
                    'mensaje': 'No hay sesión de Stripe asociada'
                })
                
        except Exception as e:
            return Response(
                {'error': f'Error verificando estado: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class OrdenCompraViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista para gestionar órdenes de compra (solo lectura)
    """
    queryset = OrdenCompra.objects.all()
    serializer_class = OrdenCompraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Los clientes solo ven sus propias órdenes
        if self.request.user.rol and self.request.user.rol.nombre == 'Cliente':
            if hasattr(self.request.user, 'cliente') and self.request.user.cliente:
                return OrdenCompra.objects.filter(cliente=self.request.user.cliente)
            return OrdenCompra.objects.none()
        
        # Administradores ven todas las órdenes
        return OrdenCompra.objects.all()

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def stripe_webhook(request):
    """
    Webhook para recibir eventos de Stripe
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = StripeService.procesar_webhook(payload, sig_header)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Procesar el evento
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        manejar_pago_exitoso(session)
    
    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
        manejar_pago_expirado(session)
    
    return Response({'status': 'success'})

def manejar_pago_exitoso(session):
    """
    Maneja un pago exitoso de Stripe
    """
    try:
        with transaction.atomic():
            # Buscar el pago por session_id
            pago = Pago.objects.get(
            stripe_checkout_session_id=session['id'],
            estado='PENDIENTE'
        )
        
        # Actualizar pago
        pago.marcar_como_completado()
        pago.stripe_payment_intent_id = session.get('payment_intent')
        pago.save()
        
        # Actualizar orden asociada
        if hasattr(pago, 'orden'):
            orden = pago.orden
            orden.estado = 'COMPLETADA'
            orden.fecha_completada = timezone.now()
            orden.save()
            
            # Si es una orden del carrito, crear ventas y vaciar carrito
            if orden.items and pago.metadata.get('tipo') == 'carrito':
                crear_ventas_desde_orden(orden)
                CarritoCompra.objects.filter(cliente=orden.cliente).delete()
        
        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=pago.cliente.usuario if hasattr(pago.cliente, 'usuario') else None,
            accion='UPDATE',
            modelo_afectado='Pago',
            id_objeto=pago.id,
            descripcion=f'Pago completado - ${pago.monto}'
        )
        
        # Aquí podrías enviar un email de confirmación
        
    except Pago.DoesNotExist:
        print(f"Pago no encontrado para session: {session['id']}")
    except Exception as e:
        print(f"Error manejando pago exitoso: {str(e)}")

def manejar_pago_expirado(session):
    """
    Maneja una sesión de pago expirada
    """
    try:
        pago = Pago.objects.get(stripe_checkout_session_id=session['id'])
        pago.estado = 'FALLIDO'
        pago.save()
        
        if hasattr(pago, 'orden'):
            orden = pago.orden
            orden.estado = 'CANCELADA'
            orden.save()
            
    except Pago.DoesNotExist:
        print(f"Pago no encontrado para session expirada: {session['id']}")

def crear_ventas_desde_orden(orden):
    """
    Crea ventas a partir de los items de una orden
    """
    for item in orden.items:
        try:
            producto = Producto.objects.get(id=item['producto_id'])
            venta = Venta.objects.create(
                cliente=orden.cliente,
                producto=producto,
                cantidad=item['cantidad'],
                precio_unitario=item['precio'],
                estado='COMPLETADA'
            )
            
            # Asignar la venta al pago si es necesario
            if hasattr(orden, 'pago') and orden.pago:
                orden.pago.venta = venta
                orden.pago.save()
                
        except Producto.DoesNotExist:
            print(f"Producto no encontrado: {item['producto_id']}")
        except Exception as e:
            print(f"Error creando venta: {str(e)}")