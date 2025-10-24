import React, { useState, useEffect } from 'react';
import { roleService } from '../../services/roles';
import { permissionService } from '../../services/permissions';

const RoleForm = ({ onRoleCreated = () => {} }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    permisos_ids: []
  });
  const [permissions, setPermissions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadPermissions();
  }, []);

  const loadPermissions = async () => {
    try {
      const data = await permissionService.getPermissions();
      setPermissions(data);
    } catch (err) {
      console.error('Error al cargar permisos:', err);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handlePermissionToggle = (permisoId) => {
    setFormData((prev) => {
      const selected = prev.permisos_ids.includes(permisoId)
        ? prev.permisos_ids.filter((id) => id !== permisoId)
        : [...prev.permisos_ids, permisoId];
      return { ...prev, permisos_ids: selected };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await roleService.createRole(formData);
      onRoleCreated();
      setFormData({ nombre: '', descripcion: '', permisos_ids: [] });
      alert('Rol creado exitosamente');
    } catch (err) {
      console.error('Error al crear rol:', err.response?.data || err);
      setError('Error al crear rol');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="role-form">
      <h3>Crear Nuevo Rol</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Nombre:</label>
          <input
            type="text"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Descripción:</label>
          <textarea
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
            rows="3"
          />
        </div>

        <div className="form-group">
          <label>Permisos:</label>
          <div className="permissions-list">
            {permissions.map((permiso) => (
              <label key={permiso.id}>
                <input
                  type="checkbox"
                  checked={formData.permisos_ids.includes(permiso.id)}
                  onChange={() => handlePermissionToggle(permiso.id)}
                />
                {permiso.nombre}
              </label>
            ))}
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <button type="submit" disabled={loading}>
          {loading ? 'Creando...' : 'Crear Rol'}
        </button>
      </form>
    </div>
  );
};

export default RoleForm;
