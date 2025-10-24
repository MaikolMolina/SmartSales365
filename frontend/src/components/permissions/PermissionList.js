import React, { useState, useEffect } from 'react';
import { permissionService } from '../../services/permissions';
import PermissionItem from './PermissionItem';
import PermissionForm from './PermissionForm';

const PermissionList = () => {
  const [permissions, setPermissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadPermissions();
  }, []);

  const loadPermissions = async () => {
    try {
      setLoading(true);
      const data = await permissionService.getPermissions();
      setPermissions(data);
    } catch (err) {
      console.error('Error al cargar permisos:', err);
      setError('Error al cargar los permisos');
    } finally {
      setLoading(false);
    }
  };

  const handlePermissionUpdated = () => {
    loadPermissions();
  };

  const handlePermissionCreated = () => {
    loadPermissions();
  };

  if (loading) return <div>Cargando permisos...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="permission-list">
      <h2>Gestión de Permisos</h2>
      <PermissionForm onPermissionCreated={handlePermissionCreated} />

      <h3>Lista de Permisos</h3>
      {permissions.length === 0 ? (
        <p>No hay permisos registrados</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Código</th>
                <th>Descripción</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {permissions.map(permiso => (
                <PermissionItem
                  key={permiso.id}
                  permiso={permiso}
                  onPermissionUpdated={handlePermissionUpdated}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default PermissionList;
