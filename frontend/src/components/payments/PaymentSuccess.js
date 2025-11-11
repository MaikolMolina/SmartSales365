import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom'; // <-- reemplazado useHistory
import { paymentService } from '../../services/payments';

const PaymentSuccess = () => {
  const [paymentInfo, setPaymentInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const location = useLocation();
  const navigate = useNavigate(); // <-- useNavigate en vez de history

  useEffect(() => {
    const checkPaymentStatus = async () => {
      const urlParams = new URLSearchParams(location.search);
      const sessionId = urlParams.get('session_id');
      const orderId = urlParams.get('orden_id');

      if (!sessionId) {
        setError('No se encontró información de la sesión de pago');
        setLoading(false);
        return;
      }

      try {
        // Simulación de verificación de pago
        setTimeout(() => {
          setPaymentInfo({
            sessionId,
            orderId,
            status: 'success',
            amount: 0,
            date: new Date().toLocaleString()
          });
          setLoading(false);
        }, 2000);

      } catch (err) {
        setError('Error verificando el estado del pago');
        setLoading(false);
      }
    };

    checkPaymentStatus();
  }, [location]);

  const continueShopping = () => {
    navigate('/productos'); // <-- reemplazado history.push
  };

  const viewOrders = () => {
    navigate('/mis-compras'); // <-- reemplazado history.push
  };

  if (loading) {
    return (
      <div className="payment-success">
        <div className="loading-payment">
          <div className="spinner"></div>
          <h2>Verificando tu pago...</h2>
          <p>Esto puede tomar unos segundos</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="payment-success">
        <div className="payment-error">
          <div className="error-icon">❌</div>
          <h2>Error en el pago</h2>
          <p>{error}</p>
          <button onClick={continueShopping} className="continue-btn">
            Volver a la tienda
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="payment-success">
      <div className="success-container">
        <div className="success-header">
          <div className="success-icon">✅</div>
          <h1>¡Pago Exitoso!</h1>
          <p>Gracias por tu compra. Tu pedido ha sido procesado correctamente.</p>
        </div>

        {paymentInfo && (
          <div className="payment-details">
            <div className="detail-card">
              <h3>Detalles del Pago</h3>
              
              <div className="detail-row">
                <span>Número de orden:</span>
                <strong>#{paymentInfo.orderId || 'N/A'}</strong>
              </div>
              
              <div className="detail-row">
                <span>Sesión de pago:</span>
                <span className="session-id">{paymentInfo.sessionId}</span>
              </div>
              
              <div className="detail-row">
                <span>Estado:</span>
                <span className="status success">Completado</span>
              </div>
              
              <div className="detail-row">
                <span>Fecha:</span>
                <span>{paymentInfo.date}</span>
              </div>
              
              {paymentInfo.amount > 0 && (
                <div className="detail-row total">
                  <span>Total pagado:</span>
                  <strong>${paymentInfo.amount}</strong>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="next-steps">
          <h3>¿Qué sigue?</h3>
          <ul>
            <li>📧 Recibirás un email de confirmación en breve</li>
            <li>🚚 Tu pedido será procesado y enviado en 24-48 horas</li>
            <li>📦 Puedes rastrear tu pedido en la sección "Mis Compras"</li>
          </ul>
        </div>

        <div className="action-buttons">
          <button onClick={continueShopping} className="secondary-btn">
            Seguir Comprando
          </button>
          <button onClick={viewOrders} className="primary-btn">
            Ver Mis Pedidos
          </button>
        </div>
      </div>
    </div>
  );
};

export default PaymentSuccess;
