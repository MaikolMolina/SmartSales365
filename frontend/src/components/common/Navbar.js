import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Logout from '../auth/Logout';

const Navbar = () => {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) return null;

  // Determinar tipo de usuario
  const isAdmin = user.rol === 'Administrador';
  const isClient = user.rol === 'Cliente';

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <Link to={isAdmin ? "/admin-home" : "/client-home"}>
          SmartSales365
        </Link>
      </div>

      <div className="nav-links">
        {isAdmin && (
          <>
            <Link 
              to="/admin-home" 
              className={location.pathname === '/admin-home' ? 'active' : ''}
            >
              🏠 Dashboard
            </Link>
            <Link 
              to="/usuarios" 
              className={location.pathname === '/usuarios' ? 'active' : ''}
            >
              👥 Usuarios
            </Link>
            <Link 
              to="/roles" 
              className={location.pathname === '/roles' ? 'active' : ''}
            >
              🛠️ Roles
            </Link>
            <Link 
              to="/permisos" 
              className={location.pathname === '/permisos' ? 'active' : ''}
            >
              🔑 Permisos
            </Link>
            <Link 
              to="/registrar-venta" 
              className={location.pathname === '/registrar-venta' ? 'active' : ''}
            >
              💰 Registrar Venta
            </Link>
            <Link 
              to="/reportes" 
              className={location.pathname === '/reportes' ? 'active' : ''}
            >
              📊 Reportes
            </Link>
            <Link 
              to="/auditoria" 
              className={location.pathname === '/auditoria' ? 'active' : ''}
            >
              📝 Auditoría
            </Link>
          </>
        )}

        {isClient && (
          <>
            <Link 
              to="/client-home" 
              className={location.pathname === '/client-home' ? 'active' : ''}
            >
              🏠 Inicio
            </Link>
            <Link 
              to="/productos" 
              className={location.pathname === '/productos' ? 'active' : ''}
            >
              🛍️ Productos
            </Link>
            <Link 
              to="/carrito" 
              className={location.pathname === '/carrito' ? 'active' : ''}
            >
              🛒 Carrito
            </Link>
            <Link 
              to="/mis-compras" 
              className={location.pathname === '/mis-compras' ? 'active' : ''}
            >
              📦 Mis Compras
            </Link>
          </>
        )}

        <Logout />
      </div>
    </nav>
  );
};

export default Navbar;
