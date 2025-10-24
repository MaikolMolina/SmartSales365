import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="dashboard">
      <h1>Dashboard - SmartSales365</h1>
      <div className="welcome-section">
        <h2>Bienvenido, {user.first_name} {user.last_name}</h2>
        <p>Rol: {user.rol_nombre}</p>
        <p>Selecciona una opción del menú para comenzar</p>
      </div>
      
      <div className="quick-stats">
        <div className="stat-card">
          <h3>Gestión de Acceso</h3>
          <p>Administra usuarios, roles y permisos del sistema</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;