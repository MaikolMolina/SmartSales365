from django.db import models
from backend.access_control.models import Usuario

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='COMPLETADA')
    fecha_venta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ventas'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre}"

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

class CarritoCompra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='carritos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='carritos')
    cantidad = models.IntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carrito_compras'
        verbose_name = 'Carrito de Compra'
        verbose_name_plural = 'Carritos de Compra'
        unique_together = ['cliente', 'producto']  # Un producto solo una vez por cliente

    def __str__(self):
        return f"Carrito {self.id} - {self.cliente.nombre}"

    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio

    def clean(self):
        # Validar que la cantidad no exceda el stock
        if self.cantidad > self.producto.stock:
            raise ValidationError(
                f'Stock insuficiente. Solo hay {self.producto.stock} unidades disponibles.'
            )

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'metodos_pago'
        verbose_name = 'Método de Pago'
        verbose_name_plural = 'Métodos de Pago'

    def __str__(self):
        return self.nombre

# Agregar el modelo ReporteGenerado aquí también para evitar dependencias circulares
class ReporteGenerado(models.Model):
    FORMATO_CHOICES = [
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
        ('JSON', 'JSON'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    prompt = models.TextField()
    formato_solicitado = models.CharField(max_length=10, choices=FORMATO_CHOICES)
    consulta_sql = models.TextField(blank=True, null=True)
    resultado = models.JSONField(blank=True, null=True)
    archivo_generado = models.FileField(upload_to='reportes/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tiempo_ejecucion = models.FloatField(blank=True, null=True)
    
    class Meta:
        db_table = 'reportes_generados'
        verbose_name = 'Reporte Generado'
        verbose_name_plural = 'Reportes Generados'
    
    def __str__(self):
        return f"Reporte {self.id} - {self.usuario.username}"
    
class Pago(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('FALLIDO', 'Fallido'),
        ('REEMBOLSADO', 'Reembolsado'),
    ]

    METODO_CHOICES = [
        ('STRIPE', 'Stripe'),
        ('PAYPAL', 'PayPal'),
    ]

    # Relaciones
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pagos')
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name='pago', null=True, blank=True)
    
    # Información del pago
    metodo_pago = models.CharField(max_length=10, choices=METODO_CHOICES, default='STRIPE')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default='USD')
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='PENDIENTE')
    
    # IDs de Stripe
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_checkout_session_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Metadatos
    descripcion = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'pagos'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Pago {self.id} - {self.cliente.nombre} - ${self.monto}"

    def marcar_como_completado(self):
        self.estado = 'COMPLETADO'
        self.fecha_pago = timezone.now()
        self.save()

    def marcar_como_fallido(self):
        self.estado = 'FALLIDO'
        self.save()

class OrdenCompra(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PROCESANDO', 'Procesando'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ordenes')
    items = models.JSONField()  # Almacena los productos del carrito
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='PENDIENTE')
    pago = models.OneToOneField(Pago, on_delete=models.SET_NULL, null=True, blank=True, related_name='orden')
    
    # Dirección de envío
    direccion_envio = models.JSONField(default=dict, blank=True)
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_completada = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'ordenes_compra'
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'

    def __str__(self):
        return f"Orden {self.id} - {self.cliente.nombre}"