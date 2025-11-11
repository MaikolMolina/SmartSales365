import api from './api';

export const saleService = {
  // Obtener todas las ventas
  getSales: () => {
    return api.get('/commercial/ventas/').then(response => response.data);
  },

  // Obtener venta por ID
  getSale: (id) => {
    return api.get(`/commercial/ventas/${id}/`).then(response => response.data);
  },

  // Crear nueva venta
  createSale: (saleData) => {
    return api.post('/commercial/ventas/', saleData).then(response => response.data);
  },

  // Actualizar venta
  updateSale: (id, saleData) => {
    return api.put(`/commercial/ventas/${id}/`, saleData).then(response => response.data);
  },

  // Eliminar venta
  deleteSale: (id) => {
    return api.delete(`/commercial/ventas/${id}/`).then(response => response.data);
  },

  // Obtener mis ventas (para clientes)
  getMySales: () => {
    return api.get('/commercial/ventas/mis_ventas/').then(response => response.data);
  },

  // Obtener estadísticas (para administradores)
  getStatistics: () => {
    return api.get('/commercial/ventas/estadisticas/').then(response => response.data);
  }
};

export const productService = {
  // Obtener todos los productos
  getProducts: () => {
    return api.get('/commercial/productos/').then(response => response.data);
  },

  // Obtener producto por ID
  getProduct: (id) => {
    return api.get(`/commercial/productos/${id}/`).then(response => response.data);
  }
};

export const clientService = {
  // Obtener perfil del cliente
  getMyProfile: () => {
    return api.get('/commercial/clientes/mi_perfil/').then(response => response.data);
  }
};

export const cartService = {
  // Obtener el carrito del usuario
  getCart: () => {
    return api.get('/commercial/carrito/mi_carrito/').then(response => response.data);
  },

  // Agregar producto al carrito
  addToCart: (productoId, cantidad = 1) => {
    return api.post('/commercial/carrito/agregar_producto/', {
      producto_id: productoId,
      cantidad: cantidad
    }).then(response => response.data);
  },

  // Actualizar cantidad en el carrito
  updateCartItem: (itemId, cantidad) => {
    return api.post(`/commercial/carrito/${itemId}/actualizar_cantidad/`, {
      cantidad: cantidad
    }).then(response => response.data);
  },

  // Eliminar item del carrito
  removeFromCart: (itemId) => {
    return api.delete(`/commercial/carrito/${itemId}/`).then(response => response.data);
  },

  // Vaciar carrito
  clearCart: () => {
    return api.post('/commercial/carrito/vaciar_carrito/').then(response => response.data);
  },

  // Obtener resumen del carrito
  getCartSummary: () => {
    return api.get('/commercial/carrito/resumen/').then(response => response.data);
  },

  // Finalizar compra
  checkout: () => {
    return api.post('/commercial/carrito/finalizar_compra/').then(response => response.data);
  }
};