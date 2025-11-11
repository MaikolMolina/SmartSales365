import React, { useState, useEffect } from 'react';
import { saleService } from '../../services/sales';

const PurchaseHistory = () => {
  const [purchases, setPurchases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadPurchases();
  }, []);

  const loadPurchases = async () => {
    try {
      const purchasesData = await saleService.getMySales();
      setPurchases(purchasesData);
    } catch (err) {
      setError('Error al cargar el historial de compras');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'COMPLETADA': { class: 'completed', label: 'Completada' },
      'PENDIENTE': { class: 'pending', label: 'Pendiente' },
      'CANCELADA': { class: 'cancelled', label: 'Cancelada' }
    };
    
    const config = statusConfig[status] || { class: 'default', label: status };
    return <span className={`status-badge ${config.class}`}>{config.label}</span>;
  };

  if (loading) {
    return <div className="loading">Cargando historial de compras...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="purchase-history">
      <h2>Mis Compras</h2>
      
      {purchases.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📦</div>
          <h3>No hay compras registradas</h3>
          <p>Aún no has realizado ninguna compra. ¡Explora nuestros productos!</p>
          <button 
            onClick={() => window.location.href = '/productos'}
            className="browse-products-btn"
          >
            Ver Productos
          </button>
        </div>
      ) : (
        <div className="purchases-list">
          {purchases.map(purchase => (
            <div key={purchase.id} className="purchase-card">
              <div className="purchase-header">
                <div className="purchase-info">
                  <h3>Compra #{purchase.id}</h3>
                  <span className="purchase-date">
                    {formatDate(purchase.fecha_venta)}
                  </span>
                </div>
                {getStatusBadge(purchase.estado)}
              </div>
              
              <div className="purchase-details">
                <div className="product-info">
                  <h4>{purchase.producto_nombre}</h4>
                  <div className="product-meta">
                    <span>Cantidad: {purchase.cantidad}</span>
                    <span>Precio unitario: ${purchase.precio_unitario}</span>
                  </div>
                </div>
                
                <div className="purchase-totals">
                  <div className="total-amount">
                    ${purchase.total || purchase.total_calculado}
                  </div>
                </div>
              </div>
              
              <div className="purchase-footer">
                <div className="delivery-info">
                  <span className="delivery-status">✅ Entregado</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PurchaseHistory;