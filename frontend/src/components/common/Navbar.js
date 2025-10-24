import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Logout from '../auth/Logout';

const Navbar = () => {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) return null;

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <Link to="/dashboard">SmartSales365</Link>
      </div>
      <div className="nav-links">
        <Link 
          to="/usuarios" 
          className={location.pathname === '/usuarios' ? 'active' : ''}
        >
          Usuarios
        </Link>
        <Link 
          to="/roles" 
          className={location.pathname === '/roles' ? 'active' : ''}
        >
          Roles
        </Link>
        <Link 
          to="/permisos" 
          className={location.pathname === '/permisos' ? 'active' : ''}
        >
          Permisos
        </Link>
        <Link 
          to="/auditoria" 
          className={location.pathname === '/auditoria' ? 'active' : ''}
        >
          Auditoría
        </Link>
        <Logout />
      </div>
    </nav>
  );
};

export default Navbar;