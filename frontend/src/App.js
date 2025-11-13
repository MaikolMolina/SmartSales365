import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Navbar from './components/common/Navbar';
import PrivateRoute from './components/common/PrivateRoute';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import UsersPage from './pages/UsersPage';
import RolesPage from './pages/RolesPage';
import PermissionsPage from './pages/PermissionsPage';
import AuditPage from './pages/AuditPage';
import ReportsPage from './pages/ReportsPage';
import Register from './components/auth/Register';
import ClientHome from './pages/ClientHome';
import AdminHome from './pages/AdminHome';
import SaleRegisterPage from './pages/SaleRegisterPage';
import ProductList from './components/products/ProductList';
import PurchaseHistory from './components/purchases/PurchaseHistory';
import Cart from './components/cart/Cart';
import CheckoutPage from './pages/CheckoutPage';
import PaymentSuccess from './components/payments/PaymentSuccess';
import PredictionDashboard from './components/PredictionDashboard';
import './components/payments/Payments.css';
import './App.css';

function AppContent() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loading-full">Cargando...</div>;
  }

  return (
    <div className="App">
      {user && <Navbar />}
      <main className={user ? 'main-with-navbar' : 'main-full'}>
        <Routes>
          {/* Rutas públicas */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<Register />} />

          {/* Rutas privadas */}
          <Route element={<PrivateRoute />}>
            {/* Rutas Admin */}
            <Route
              path="/admin-home"
              element={user?.rol === 'Administrador' ? <AdminHome /> : <Navigate to="/client-home" replace />}
            />
            <Route
              path="/registrar-venta"
              element={user?.rol === 'Administrador' ? <SaleRegisterPage /> : <Navigate to="/client-home" replace />}
            />
            <Route
              path="/usuarios"
              element={user?.rol === 'Administrador' ? <UsersPage /> : <Navigate to="/client-home" replace />}
            />
            <Route
              path="/roles"
              element={user?.rol === 'Administrador' ? <RolesPage /> : <Navigate to="/client-home" replace />}
            />
            <Route
              path="/permisos"
              element={user?.rol === 'Administrador' ? <PermissionsPage /> : <Navigate to="/client-home" replace />}
            />
            <Route
              path="/auditoria"
              element={user?.rol === 'Administrador' ? <AuditPage /> : <Navigate to="/client-home" replace />}
            />
            <Route
              path="/reportes"
              element={user?.rol === 'Administrador' ? <ReportsPage /> : <Navigate to="/client-home" replace />}
            />
            <Route
              path="/predictions"
              element={user?.rol === 'Administrador' ? <PredictionDashboard /> : <Navigate to="/client-home" replace />}
            />

            {/* Rutas Cliente */}
            <Route
              path="/client-home"
              element={user?.rol === 'Cliente' ? <ClientHome /> : <Navigate to="/admin-home" replace />}
            />
            <Route
              path="/productos"
              element={user?.rol === 'Cliente' ? <ProductList /> : <Navigate to="/admin-home" replace />}
            />
            <Route
              path="/carrito"  
              element={user?.rol === 'Cliente' ? <Cart /> : <Navigate to="/admin-home" replace />}
            />
            <Route
              path="/mis-compras"
              element={user?.rol === 'Cliente' ? <PurchaseHistory /> : <Navigate to="/admin-home" replace />}
            />
            <Route
              path="/checkout"
              element={user?.rol === 'Cliente' ? <CheckoutPage /> : <Navigate to="/admin-home" replace />}
            />
            <Route
              path="/payment-success"
              element={user?.rol === 'Cliente' ? <PaymentSuccess /> : <Navigate to="/admin-home" replace />}
            />

            {/* Dashboard genérico */}
            <Route
              path="/dashboard"
              element={
                user?.rol === 'Administrador' ? <AdminHome /> : <ClientHome />
              }
            />
          </Route>

          {/* Redirección raíz */}
          <Route
            path="/"
            element={
              <Navigate
                to={user ? (user.rol === 'Administrador' ? '/admin-home' : '/client-home') : '/login'}
                replace
              />
            }
          />

          {/* Cualquier ruta no existente */}
          <Route
            path="*"
            element={
              <Navigate
                to={user ? (user.rol === 'Administrador' ? '/admin-home' : '/client-home') : '/login'}
                replace
              />
            }
          />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;
