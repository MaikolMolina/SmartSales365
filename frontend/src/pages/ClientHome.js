import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import ProductList from '../components/products/ProductList';

const ClientHome = () => {
  const { user } = useAuth();

  return (
    <div className="client-home">
      <div className="welcome-section">
        <h1>Bienvenido, {user.first_name} {user.last_name}</h1>
        <p>Explora nuestro catálogo de productos y encuentra lo que necesitas</p>
        <div className="client-stats">
          <div className="stat-card">
            <h3>🎁 Productos Disponibles</h3>
            <p>Descubre nuestra amplia variedad</p>
          </div>
          <div className="stat-card">
            <h3>🚚 Envío Rápido</h3>
            <p>Recibe tus productos en 24-48h</p>
          </div>
          <div className="stat-card">
            <h3>💳 Pago Seguro</h3>
            <p>Múltiples métodos de pago</p>
          </div>
        </div>
      </div>

      <ProductList />
    </div>
  );
};

export default ClientHome;