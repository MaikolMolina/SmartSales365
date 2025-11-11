import stripe
from django.conf import settings
from django.urls import reverse
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    """
    Servicio para manejar operaciones con Stripe
    """
    
    @staticmethod
    def crear_sesion_pago(orden_compra, success_url, cancel_url, metadata=None):
        """
        Crea una sesión de Checkout de Stripe
        """
        try:
            # Convertir items del carrito a formato de línea de Stripe
            line_items = []
            for item in orden_compra.items:
                # Solo incluir 'description' si no está vacío
                product_data = {
                    'name': item['producto_nombre'],
                    **({'description': item['descripcion']} if item.get('descripcion') else {}),
                    'metadata': {
                        'producto_id': item['producto_id']
                    }
                }
                
                line_item = {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': product_data,
                        'unit_amount': int(Decimal(str(item['precio'])) * 100),  # Convertir a centavos
                    },
                    'quantity': item['cantidad'],
                }
                line_items.append(line_item)
            
            # Crear sesión de checkout
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=orden_compra.cliente.email,
                metadata={
                    'orden_id': str(orden_compra.id),
                    'cliente_id': str(orden_compra.cliente.id),
                    **(metadata or {})
                },
                shipping_address_collection={
                    'allowed_countries': ['US', 'CA', 'MX', 'ES', 'CO', 'AR', 'BR', 'CL', 'PE']
                },
                automatic_tax={'enabled': True},
            )
            
            return checkout_session
            
        except stripe.error.StripeError as e:
            raise Exception(f"Error de Stripe: {str(e)}")
        except Exception as e:
            raise Exception(f"Error creando sesión de pago: {str(e)}")
    
    @staticmethod
    def crear_sesion_pago_simple(monto, descripcion, success_url, cancel_url, metadata=None):
        """
        Crea una sesión de pago simple (sin orden de compra)
        """
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': descripcion,
                        },
                        'unit_amount': int(monto * 100),  # Convertir a centavos
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata or {},
            )
            
            return checkout_session
            
        except stripe.error.StripeError as e:
            raise Exception(f"Error de Stripe: {str(e)}")
        except Exception as e:
            raise Exception(f"Error creando sesión de pago: {str(e)}")
    
    @staticmethod
    def obtener_sesion(session_id):
        """
        Obtiene los detalles de una sesión de Stripe
        """
        try:
            return stripe.checkout.Session.retrieve(session_id)
        except stripe.error.StripeError as e:
            raise Exception(f"Error obteniendo sesión de Stripe: {str(e)}")
    
    @staticmethod
    def crear_payment_intent(monto, metadata=None):
        """
        Crea un Payment Intent para pagos personalizados
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(monto * 100),
                currency='usd',
                metadata=metadata or {},
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return intent
        except stripe.error.StripeError as e:
            raise Exception(f"Error creando payment intent: {str(e)}")
    
    @staticmethod
    def procesar_webhook(payload, sig_header):
        """
        Procesa webhooks de Stripe
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            raise Exception(f"Payload inválido: {str(e)}")
        except stripe.error.SignatureVerificationError as e:
            raise Exception(f"Firma inválida: {str(e)}")
