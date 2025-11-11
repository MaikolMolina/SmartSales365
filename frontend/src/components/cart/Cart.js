import React, { useState, useEffect } from 'react';
import { cartService } from '../../services/sales';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom'; 

const Cart = () => {
  const { user } = useAuth();
  const [cart, setCart] = useState({ items: [], resumen: {} });
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [processing, setProcessing] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadCart();
  }, []);

  const loadCart = async () => {
    try {
      const cartData = await cartService.getCart();
      setCart(cartData);
    } catch (error) {
      console.error('Error cargando carrito:', error);
      setMessage('Error al cargar el carrito');
    } finally {
      setLoading(false);
    }
  };

  const updateQuantity = async (itemId, newQuantity) => {
    if (newQuantity < 1) return;

    try {
      await cartService.updateCartItem(itemId, newQuantity);
      await loadCart(); // Recargar carrito
      setMessage('Cantidad actualizada');
    } catch (error) {
      setMessage(error.response?.data?.error || 'Error actualizando cantidad');
    }
  };

  const removeItem = async (itemId) => {
    try {
      await cartService.removeFromCart(itemId);
      await loadCart(); // Recargar carrito
      setMessage('Producto eliminado del carrito');
    } catch (error) {
      setMessage('Error eliminando producto del carrito');
    }
  };

  const clearCart = async () => {
    if (window.confirm('¿Estás seguro de que quieres vaciar el carrito?')) {
      try {
        await cartService.clearCart();
        await loadCart();
        setMessage('Carrito vaciado');
      } catch (error) {
        setMessage('Error vaciando el carrito');
      }
    }
  };

  const handleCheckout = async () => {
    if (!cart.items.length) {
      setMessage('El carrito está vacío');
      return;
    }

    setProcessing(true);
    try {
      const result = await cartService.checkout();
      setMessage(`✅ ${result.message}. Total: $${result.total_compra}`);
      await loadCart(); // Recargar carrito vacío
      
      // Redirigir al historial de compras después de 2 segundos
      setTimeout(() => {
        window.location.href = '/mis-compras';
      }, 2000);
      
    } catch (error) {
      setMessage(error.response?.data?.error || 'Error procesando la compra');
    } finally {
      setProcessing(false);
    }
  };

  const proceedToCheckout = () => {
    //window.location.href = '/checkout';
    navigate('/checkout');
  };

  const continueShopping = () => {
    //window.location.href = '/productos';
    navigate('/productos');
  };

  if (loading) {
    return <div className="loading">Cargando carrito...</div>;
  }

  return (
    <div className="cart-page">
      <div className="cart-header">
        <h1>🛒 Mi Carrito de Compras</h1>
        <p>Revisa y gestiona los productos en tu carrito</p>
      </div>

      {message && (
        <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}

      {cart.items.length === 0 ? (
        <div className="empty-cart">
          <div className="empty-icon">🛒</div>
          <h2>Tu carrito está vacío</h2>
          <p>Agrega algunos productos increíbles a tu carrito</p>
          <button onClick={continueShopping} className="continue-shopping-btn">
            Continuar Comprando
          </button>
        </div>
      ) : (
        <div className="cart-content">
          <div className="cart-items">
            <h3>Productos en el carrito ({cart.resumen.total_items})</h3>
            
            {cart.items.map(item => (
              <div key={item.id} className="cart-item">
                <div className="item-image">
                  {item.producto_imagen ? (
                    <img src={item.producto_imagen} alt={item.producto_nombre} />
                  ) : (
                    <div className="image-placeholder">📦</div>
                  )}
                </div>
                
                <div className="item-details">
                  <h4>{item.producto_nombre}</h4>
                  <p className="item-price">${item.producto_precio} c/u</p>
                  <p className="stock-info">
                    Stock disponible: {item.producto_stock} unidades
                  </p>
                </div>
                
                <div className="item-controls">
                  <div className="quantity-controls">
                    <button 
                      onClick={() => updateQuantity(item.id, item.cantidad - 1)}
                      disabled={item.cantidad <= 1}
                      className="quantity-btn"
                    >
                      -
                    </button>
                    <span className="quantity">{item.cantidad}</span>
                    <button 
                      onClick={() => updateQuantity(item.id, item.cantidad + 1)}
                      disabled={item.cantidad >= item.producto_stock}
                      className="quantity-btn"
                    >
                      +
                    </button>
                  </div>
                  
                  <div className="item-subtotal">
                    ${item.subtotal}
                  </div>
                  
                  <button 
                    onClick={() => removeItem(item.id)}
                    className="remove-btn"
                    title="Eliminar del carrito"
                  >
                    🗑️
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="cart-summary">
            <div className="summary-card">
              <h3>Resumen de la Compra</h3>
              
              <div className="summary-row">
                <span>Productos:</span>
                <span>{cart.resumen.total_items}</span>
              </div>
              
              <div className="summary-row">
                <span>Total unidades:</span>
                <span>{cart.resumen.total_cantidad}</span>
              </div>
              
              <div className="summary-row total">
                <span>Total a pagar:</span>
                <span>${cart.resumen.total_precio}</span>
              </div>
              
              <div className="summary-actions">
                <button 
                  onClick={clearCart}
                  className="clear-cart-btn"
                >
                  Vaciar Carrito
                </button>
                
                <button 
                  onClick={proceedToCheckout}
                  disabled={processing || !cart.items.length}
                  className="checkout-btn"
                >
                  {processing ? 'Procesando...' : 'Proceder al Pago'}
                </button>
              </div>
              
              <div className="security-notice">
                <p>🔒 Compra 100% segura. Tus datos están protegidos.</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Cart;