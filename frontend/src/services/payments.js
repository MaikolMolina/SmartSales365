import api from './api';

export const paymentService = {
  // Crear sesión de pago desde el carrito
  createPaymentFromCart: () => {
    return api.post('/commercial/pagos/pago_desde_carrito/').then(response => response.data);
  },

  // Crear sesión de pago para una orden específica
  createPaymentSession: (ordenId, monto, descripcion) => {
    const data = {};
    if (ordenId) {
      data.orden_id = ordenId;
    } else {
      data.monto = monto;
      data.descripcion = descripcion;
    }
    
    return api.post('/commercial/pagos/crear_sesion_pago/', data).then(response => response.data);
  },

  // Verificar estado de un pago
  verifyPaymentStatus: (pagoId) => {
    return api.get(`/commercial/pagos/${pagoId}/verificar_estado/`).then(response => response.data);
  },

  // Obtener información de un pago
  getPayment: (pagoId) => {
    return api.get(`/commercial/pagos/${pagoId}/`).then(response => response.data);
  },

  // Obtener órdenes del usuario
  getMyOrders: () => {
    return api.get('/commercial/ordenes/').then(response => response.data);
  },

  // Obtener una orden específica
  getOrder: (ordenId) => {
    return api.get(`/commercial/ordenes/${ordenId}/`).then(response => response.data);
  }
};

// Configuración de Stripe
export const loadStripe = () => {
  return window.Stripe('pk_test_51SKTrqHwD6XEzQHGrv5BhO2Vy9dzEGmnGrMki66qEN0J9AluwMFrXTkAXC0KbulFejX81u2JnC4tIQom9KetNtPS00l67fBQJb'); // Tu clave pública de Stripe
};