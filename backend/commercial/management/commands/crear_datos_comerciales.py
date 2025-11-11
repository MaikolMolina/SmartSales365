from django.core.management.base import BaseCommand
from backend.commercial.models import Categoria, Producto, Cliente, Venta
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Crea datos de prueba para el módulo comercial'

    def handle(self, *args, **options):
        # Crear categorías
        categorias_data = [
            {'nombre': 'Electrónicos', 'descripcion': 'Dispositivos electrónicos'},
            {'nombre': 'Ropa', 'descripcion': 'Prendas de vestir'},
            {'nombre': 'Hogar', 'descripcion': 'Artículos para el hogar'},
            {'nombre': 'Deportes', 'descripcion': 'Equipos deportivos'},
        ]
        
        categorias = []
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(**cat_data)
            categorias.append(categoria)
            if created:
                self.stdout.write(f'Categoría creada: {categoria.nombre}')

        # Crear productos
        productos_data = [
            {'nombre': 'Smartphone', 'categoria': categorias[0], 'precio': 599.99, 'stock': 50},
            {'nombre': 'Laptop', 'categoria': categorias[0], 'precio': 899.99, 'stock': 30},
            {'nombre': 'Auriculares', 'categoria': categorias[0], 'precio': 99.99, 'stock': 100},
            {'nombre': 'Camiseta', 'categoria': categorias[1], 'precio': 29.99, 'stock': 200},
            {'nombre': 'Pantalón', 'categoria': categorias[1], 'precio': 49.99, 'stock': 150},
            {'nombre': 'Silla Oficina', 'categoria': categorias[2], 'precio': 199.99, 'stock': 25},
            {'nombre': 'Mesa', 'categoria': categorias[2], 'precio': 299.99, 'stock': 15},
            {'nombre': 'Pelota Fútbol', 'categoria': categorias[3], 'precio': 39.99, 'stock': 80},
            {'nombre': 'Raqueta Tenis', 'categoria': categorias[3], 'precio': 89.99, 'stock': 40},
        ]
        
        productos = []
        for prod_data in productos_data:
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults=prod_data
            )
            productos.append(producto)
            if created:
                self.stdout.write(f'Producto creado: {producto.nombre}')

        # Crear clientes
        clientes_data = [
            {'nombre': 'Juan Pérez', 'email': 'juan@email.com', 'telefono': '+1234567890'},
            {'nombre': 'María García', 'email': 'maria@email.com', 'telefono': '+1234567891'},
            {'nombre': 'Carlos López', 'email': 'carlos@email.com', 'telefono': '+1234567892'},
            {'nombre': 'Ana Martínez', 'email': 'ana@email.com', 'telefono': '+1234567893'},
            {'nombre': 'Pedro Rodríguez', 'email': 'pedro@email.com', 'telefono': '+1234567894'},
        ]
        
        clientes = []
        for cli_data in clientes_data:
            cliente, created = Cliente.objects.get_or_create(
                email=cli_data['email'],
                defaults=cli_data
            )
            clientes.append(cliente)
            if created:
                self.stdout.write(f'Cliente creado: {cliente.nombre}')

        # Crear ventas de prueba (últimos 6 meses)
        ventas_creadas = 0
        for i in range(100):  # 100 ventas de prueba
            cliente = random.choice(clientes)
            producto = random.choice(productos)
            cantidad = random.randint(1, 5)
            precio_unitario = producto.precio
            fecha_venta = datetime.now() - timedelta(days=random.randint(1, 180))
            
            venta, created = Venta.objects.get_or_create(
                cliente=cliente,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                fecha_venta=fecha_venta,
                defaults={'estado': 'COMPLETADA'}
            )
            
            if created:
                ventas_creadas += 1

        self.stdout.write(
            self.style.SUCCESS(f'Datos comerciales creados: {ventas_creadas} ventas generadas')
        )