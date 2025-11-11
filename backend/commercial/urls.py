from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import product_views
from .views import client_views
from .views import sale_views
from .views import cart_views
from .views import payment_views

router = DefaultRouter()
router.register(r'productos', product_views.ProductoViewSet, basename='producto')
router.register(r'clientes', client_views.ClienteViewSet, basename='cliente')
router.register(r'ventas', sale_views.VentaViewSet, basename='venta')
router.register(r'carrito', cart_views.CarritoCompraViewSet, basename='carrito')  
router.register(r'pagos', payment_views.PagoViewSet, basename='pago')  
router.register(r'ordenes', payment_views.OrdenCompraViewSet, basename='orden')


urlpatterns = [
    path('', include(router.urls)),
    path('stripe-webhook/', payment_views.stripe_webhook, name='stripe-webhook'),
]