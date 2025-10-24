import React, { useState, useEffect } from 'react';
import { roleService } from '../../services/roles';
import { permissionService } from '../../services/permissions';

const RoleItem = ({ rol, onRoleUpdated }) => {
  const [editing, setEditing] = useState(false);
  const [permissions, setPermissions] = useState([]);
  const [formData, setFormData] = useState({
    ...rol,
    permisos_ids: rol.permisos ? rol.permisos.map(p => p.id) : []
  });
  const [loading, setLoading] = useState(false);

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

  const handleSave = async () => {
    try {
      setLoading(true);
      const payload = {
        nombre: formData.nombre,
        descripcion: formData.descripcion,
        activo: formData.activo,
        permisos_ids: formData.permisos_ids
      };
      await roleService.updateRole(rol.id, payload);
      setEditing(false);
      onRoleUpdated();
    } catch (err) {
      console.error('Error al actualizar rol:', err.response?.data || err);
      alert('Error al actualizar rol');
    } finally {
      setLoading(false);
    }
  };


  const handleDelete = async () => {
    if (window.confirm(`¿Estás seguro de desactivar el rol "${rol.nombre}"?`)) {
      try {
        setLoading(true);
        await roleService.deleteRole(rol.id);
        onRoleUpdated();
      } catch (err) {
        console.error('Error al eliminar rol:', err);
        alert('Error al eliminar rol');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleCancel = () => {
    setFormData({
      ...rol,
      permisos_ids: rol.permisos ? rol.permisos.map(p => p.id) : []
    });
    setEditing(false);
  };

  if (editing) {
    return (
      <tr>
        <td>
          <input
            type="text"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
          />
        </td>
        <td>
          <textarea
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
            rows="2"
          />
        </td>
        <td>
          <div className="permissions-edit-list">
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
        </td>
        <td>
          <select
            name="activo"
            value={formData.activo}
            onChange={handleChange}
          >
            <option value={true}>Activo</option>
            <option value={false}>Inactivo</option>
          </select>
        </td>
        <td>
          <button onClick={handleSave} disabled={loading}>Guardar</button>
          <button onClick={handleCancel} disabled={loading}>Cancelar</button>
        </td>
      </tr>
    );
  }

  return (
    <tr>
      <td>{rol.nombre}</td>
      <td>{rol.descripcion}</td>
      <td>
        {rol.permisos && rol.permisos.length > 0
          ? rol.permisos.map(p => p.nombre).join(', ')
          : 'Sin permisos'}
      </td>
      <td>{rol.activo ? 'Activo' : 'Inactivo'}</td>
      <td>
        <button onClick={() => setEditing(true)}>Editar</button>
        <button onClick={handleDelete} className="delete-button">Eliminar</button>
      </td>
    </tr>
  );
};

export default RoleItem;
