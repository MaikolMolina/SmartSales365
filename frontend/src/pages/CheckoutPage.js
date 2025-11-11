import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { cartService } from '../services/sales';
import { paymentService } from '../services/payments';
import { useAuth } from '../contexts/AuthContext';

const CheckoutPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [cart, setCart] = useState({ items: [], resumen: { total_precio: 0 } });
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

  // Cargar carrito
  useEffect(() => {
    const loadCart = async () => {
      try {
        const cartData = await cartService.getCart();
        console.log('Carrito cargado:', cartData);
        setCart({
          items: cartData.items || [],
          resumen: cartData.resumen || { total_precio: 0 },
        });
      } catch (error) {
        console.error('Error cargando carrito:', error);
        setCart({ items: [], resumen: { total_precio: 0 } });
      } finally {
        setLoading(false);
      }
    };

    loadCart();
  }, []);

  // Procesar pago
  const processPayment = async () => {
    console.log('Botón de pago presionado');
    if (!cart.items.length) {
      alert('El carrito está vacío');
      return;
    }

    setProcessing(true);

    try {
      const paymentData = await paymentService.createPaymentFromCart();
      console.log('Respuesta del backend:', paymentData);

      if (!paymentData || !paymentData.url_pago) {
        throw new Error('No se pudo obtener la URL de pago de Stripe');
      }

      // Redirigir a Stripe Checkout
      window.location.assign(paymentData.url_pago);

    } catch (error) {
      console.error('Error procesando pago:', error);
      alert(
        error.response?.data?.error ||
        error.message ||
        'Ocurrió un error procesando el pago'
      );
      setProcessing(false);
    }
  };

  const continueShopping = () => {
    navigate('/productos');
  };

  // Render loading
  if (loading) return <div className="loading">Cargando checkout...</div>;

  // Render carrito vacío
  if (!cart.items.length) {
    return (
      <div className="checkout-page">
        <div className="empty-checkout">
          <h2>Carrito Vacío</h2>
          <p>No hay productos para procesar el pago</p>
          <button onClick={continueShopping} className="continue-btn">
            Continuar Comprando
          </button>
        </div>
      </div>
    );
  }

  // Render checkout
  return (
    <div className="checkout-page">
      <div className="checkout-container">
        <div className="checkout-header">
          <h1>Finalizar Compra</h1>
          <p>Revisa tu pedido y completa el pago</p>
        </div>

        <div className="checkout-content">
          <div className="order-summary">
            <h3>Resumen del Pedido</h3>
            <div className="order-items">
              {(cart.items || []).map(item => (
                <div key={item.id} className="order-item">
                  <div className="item-info">
                    <h4>{item.producto_nombre}</h4>
                    <p>Cantidad: {item.cantidad}</p>
                  </div>
                  <div className="item-price">${(item.subtotal || 0).toFixed(2)}</div>
                </div>
              ))}

            <p><strong>Nombre:</strong> {user ? `${user.first_name} ${user.last_name}` : 'Invitado'}</p>
            <p><strong>Email:</strong> {user?.email || 'No proporcionado'}</p>

            </div>

            <div className="order-totals">
              <div className="total-row">
                <span>Subtotal:</span>
                <span>${cart.resumen.total_precio.toFixed(2)}</span>
              </div>
              <div className="total-row">
                <span>Envío:</span>
                <span>$0.00</span>
              </div>
              <div className="total-row">
                <span>Impuestos:</span>
                <span>$0.00</span>
              </div>
              <div className="total-row grand-total">
                <span>Total:</span>
                <span>${cart.resumen.total_precio.toFixed(2)}</span>
              </div>
            </div>
          </div>

          <div className="payment-section">
            <div className="payment-methods">
              <h3>Método de Pago</h3>
              <div className="payment-option selected">
                <div className="payment-icon">💳</div>
                <div className="payment-info">
                  <h4>Tarjeta de Crédito/Débito</h4>
                  <p>Pago seguro con Stripe</p>
                </div>
              </div>

              <div className="stripe-checkout-container">
                <button
                  onClick={processPayment}
                  disabled={processing}
                  className="stripe-pay-button"
                >
                  {processing ? 'Procesando...' : `Pagar $${cart.resumen.total_precio.toFixed(2)}`}
                </button>

                <div className="payment-security">
                  <p>🔒 Tu pago está protegido con encriptación SSL</p>
                  <div className="payment-badges">
                    <span className="badge">Visa</span>
                    <span className="badge">Mastercard</span>
                    <span className="badge">Amex</span>
                    <span className="badge">Stripe</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="customer-info">
              <h3>Información del Cliente</h3>
              <div className="info-card">
                <p><strong>Nombre:</strong> {user.first_name} {user.last_name}</p>
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>Teléfono:</strong> {user.telefono || 'No proporcionado'}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="checkout-footer">
          <button onClick={continueShopping} className="back-btn">
            ← Seguir Comprando
          </button>
        </div>
      </div>
    </div>
  );
};

export default CheckoutPage;
