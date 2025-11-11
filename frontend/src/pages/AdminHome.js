import React, { useState, useEffect } from 'react';
import { saleService } from '../services/sales';
import { useAuth } from '../contexts/AuthContext';

const AdminHome = () => {
  const { user } = useAuth();
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    try {
      const stats = await saleService.getStatistics();
      setStatistics(stats);
    } catch (error) {
      console.error('Error cargando estadísticas:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Cargando estadísticas...</div>;
  }

  return (
    <div className="admin-home">
      <div className="welcome-section">
        <h1>Panel de Administración</h1>
        <p>Bienvenido, {user.first_name} {user.last_name}</p>
      </div>

      {statistics && (
        <div className="stats-grid">
          <div className="stat-card admin">
            <h3>📊 Ventas Totales</h3>
            <div className="stat-number">{statistics.total_ventas}</div>
            <p>Total de transacciones</p>
          </div>

          <div className="stat-card admin">
            <h3>💰 Ingresos Totales</h3>
            <div className="stat-number">${statistics.ingresos_totales.toFixed(2)}</div>
            <p>Ingresos acumulados</p>
          </div>

          <div className="stat-card admin">
            <h3>📈 Ventas del Mes</h3>
            <div className="stat-number">{statistics.ventas_ultimo_mes}</div>
            <p>Últimos 30 días</p>
          </div>

          <div className="stat-card admin">
            <h3>💵 Ingresos del Mes</h3>
            <div className="stat-number">${statistics.ingresos_ultimo_mes.toFixed(2)}</div>
            <p>Últimos 30 días</p>
          </div>

          <div className="stat-card admin">
            <h3>🏆 Producto Más Vendido</h3>
            <div className="stat-number">
              {statistics.producto_mas_vendido?.producto__nombre || 'N/A'}
            </div>
            <p>
              {statistics.producto_mas_vendido ? 
                `${statistics.producto_mas_vendido.total} unidades` : 
                'Sin datos'
              }
            </p>
          </div>

          <div className="stat-card admin">
            <h3>📦 Promedio de Venta</h3>
            <div className="stat-number">${statistics.promedio_venta.toFixed(2)}</div>
            <p>Por transacción</p>
          </div>
        </div>
      )}

      <div className="quick-actions">
        <h2>Acciones Rápidas</h2>
        <div className="actions-grid">
          <div className="action-card">
            <h3>➕ Registrar Venta</h3>
            <p>Registrar una nueva venta manualmente</p>
            <button 
              onClick={() => window.location.href = '/registrar-venta'}
              className="action-button"
            >
              Ir a Registrar Venta
            </button>
          </div>

          <div className="action-card">
            <h3>👥 Gestionar Clientes</h3>
            <p>Ver y administrar clientes del sistema</p>
            <button className="action-button">
              Ver Clientes
            </button>
          </div>

          <div className="action-card">
            <h3>📦 Gestionar Productos</h3>
            <p>Administrar inventario y productos</p>
            <button className="action-button">
              Ver Productos
            </button>
          </div>

          <div className="action-card">
            <h3>📊 Ver Reportes</h3>
            <p>Generar reportes dinámicos</p>
            <button 
              onClick={() => window.location.href = '/reportes'}
              className="action-button"
            >
              Ir a Reportes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminHome;