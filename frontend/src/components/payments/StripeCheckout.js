import React, { useState, useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { paymentService } from '../../services/payments';

// Cargar Stripe (reemplaza con tu clave pública)
const stripePromise = loadStripe('pk_test_51...');

const StripeCheckout = ({ orderId, amount, description, onSuccess, onCancel }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCheckout = async () => {
    setLoading(true);
    setError('');

    try {
      // Crear sesión de pago en el backend
      const sessionData = await paymentService.createPaymentSession(orderId, amount, description);
      
      // Redirigir a Stripe Checkout
      const stripe = await stripePromise;
      const { error } = await stripe.redirectToCheckout({
        sessionId: sessionData.session_id,
      });

      if (error) {
        setError(error.message);
        if (onCancel) onCancel();
      }
      
    } catch (err) {
      setError(err.response?.data?.error || 'Error iniciando el pago');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="stripe-checkout">
      <button 
        onClick={handleCheckout}
        disabled={loading}
        className="stripe-checkout-button"
      >
        {loading ? 'Procesando...' : 'Pagar con Stripe'}
      </button>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      <div className="payment-security">
        <p>🔒 Pago seguro procesado por Stripe</p>
      </div>
    </div>
  );
};

export default StripeCheckout;