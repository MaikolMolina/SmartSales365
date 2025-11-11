from rest_framework import serializers
from .models import Categoria, Producto, Cliente, Venta, CarritoCompra, Pago, OrdenCompra

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'activo']

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'categoria', 'categoria_nombre',
            'precio', 'stock', 'activo', 'fecha_creacion'
        ]

class ClienteSerializer(serializers.ModelSerializer):
    usuario_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'nombre', 'email', 'telefono', 'direccion', 
            'activo', 'fecha_creacion', 'usuario_info'
        ]
    
    def get_usuario_info(self, obj):
        if hasattr(obj, 'usuario') and obj.usuario:
            return {
                'id': obj.usuario.id,
                'username': obj.usuario.username
            }
        return None

class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    total_calculado = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Venta
        fields = [
            'id', 'cliente', 'cliente_nombre', 'producto', 'producto_nombre',
            'cantidad', 'precio_unitario', 'total', 'total_calculado',
            'estado', 'fecha_venta', 'fecha_actualizacion'
        ]
        read_only_fields = ['total', 'fecha_venta', 'fecha_actualizacion']
    
    def get_total_calculado(self, obj):
        return obj.cantidad * obj.precio_unitario
    
    def validate(self, data):
        # Validar stock disponible
        if 'producto' in data and 'cantidad' in data:
            producto = data['producto']
            cantidad = data['cantidad']
            
            if cantidad > producto.stock:
                raise serializers.ValidationError(
                    f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.'
                )
        
        return data

class CarritoCompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_precio = serializers.DecimalField(source='producto.precio', read_only=True, max_digits=10, decimal_places=2)
    producto_stock = serializers.IntegerField(source='producto.stock', read_only=True)
    producto_imagen = serializers.CharField(source='producto.imagen', read_only=True, allow_null=True)
    subtotal = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = CarritoCompra
        fields = [
            'id', 'cliente', 'producto', 'producto_nombre', 'producto_precio',
            'producto_stock', 'producto_imagen', 'cantidad', 'subtotal',
            'fecha_agregado', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_agregado', 'fecha_actualizacion']
    
    def get_subtotal(self, obj):
        return obj.cantidad * obj.producto.precio
    
    def validate(self, data):
        # Validar stock disponible
        if 'producto' in data and 'cantidad' in data:
            producto = data['producto']
            cantidad = data['cantidad']
            
            if cantidad > producto.stock:
                raise serializers.ValidationError(
                    f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.'
                )
        
        return data

class AgregarAlCarritoSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1, default=1)

class ActualizarCantidadSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(min_value=1)

class PagoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    venta_id = serializers.IntegerField(source='venta.id', read_only=True, allow_null=True)

    class Meta:
        model = Pago
        fields = [
            'id', 'cliente', 'cliente_nombre', 'venta', 'venta_id',
            'metodo_pago', 'monto', 'moneda', 'estado',
            'stripe_payment_intent_id', 'stripe_checkout_session_id',
            'descripcion', 'fecha_creacion', 'fecha_pago'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_pago']

class OrdenCompraSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    items_detallados = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrdenCompra
        fields = [
            'id', 'cliente', 'cliente_nombre', 'items', 'items_detallados',
            'total', 'estado', 'pago', 'direccion_envio',
            'fecha_creacion', 'fecha_completada'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_completada']

    def get_items_detallados(self, obj):
        # Aquí puedes enriquecer los items con información adicional si es necesario
        return obj.items

class CrearSesionPagoSerializer(serializers.Serializer):
    orden_id = serializers.IntegerField(required=False)
    monto = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    descripcion = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        if 'orden_id' not in data and 'monto' not in data:
            raise serializers.ValidationError(
                'Debe proporcionar orden_id o monto para crear una sesión de pago.'
            )
        return data