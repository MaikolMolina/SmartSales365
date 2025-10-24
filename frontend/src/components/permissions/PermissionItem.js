import React, { useState } from 'react';
import { permissionService } from '../../services/permissions';

const PermissionItem = ({ permiso, onPermissionUpdated }) => {
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState(permiso);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value
    });
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      await permissionService.updatePermission(permiso.id, formData);
      setEditing(false);
      onPermissionUpdated();
    } catch (error) {
      console.error('Error al actualizar permiso:', error);
      alert('Error al actualizar permiso');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`¿Estás seguro de desactivar el permiso "${permiso.nombre}"?`)) {
      try {
        setLoading(true);
        await permissionService.deletePermission(permiso.id);
        onPermissionUpdated();
      } catch (error) {
        console.error('Error al eliminar permiso:', error);
        alert('Error al eliminar permiso');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleCancel = () => {
    setFormData(permiso);
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
          <input
            type="text"
            name="codigo"
            value={formData.codigo}
            onChange={handleChange}
          />
        </td>
        <td>
          <textarea
            name="descripcion"
            value={formData.descripcion || ''}
            onChange={handleChange}
            rows="2"
          />
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
      <td>{permiso.nombre}</td>
      <td>{permiso.codigo}</td>
      <td>{permiso.descripcion}</td>
      <td>{permiso.activo ? 'Activo' : 'Inactivo'}</td>
      <td>
        <button onClick={() => setEditing(true)}>Editar</button>
        <button onClick={handleDelete} className="delete-button">Eliminar</button>
      </td>
    </tr>
  );
};

export default PermissionItem;
