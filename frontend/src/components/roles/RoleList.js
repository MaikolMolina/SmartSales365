import React, { useState, useEffect } from 'react';
import { roleService } from '../../services/roles';
import RoleItem from './RoleItem';
import RoleForm from './RoleForm';

const RoleList = () => {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadRoles();
  }, []);

  const loadRoles = async () => {
    try {
      setLoading(true);
      const data = await roleService.getRoles();
      setRoles(data);
    } catch (err) {
      console.error('Error al cargar roles:', err);
      setError('Error al cargar roles');
    } finally {
      setLoading(false);
    }
  };

  const handleRoleUpdated = () => {
    loadRoles();
  };

  const handleRoleCreated = () => {
    loadRoles();
  };

  if (loading) return <div>Cargando roles...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="role-list">
      <h2>Gestión de Roles</h2>
      <RoleForm onRoleCreated={handleRoleCreated} />

      <h3>Lista de Roles</h3>
      {roles.length === 0 ? (
        <p>No hay roles registrados</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Descripción</th>
                <th>Permisos</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {roles.map((rol) => (
                <RoleItem
                  key={rol.id}
                  rol={rol}
                  onRoleUpdated={handleRoleUpdated}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default RoleList;
