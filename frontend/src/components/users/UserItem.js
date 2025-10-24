import React, { useState } from 'react';
import { userService } from '../../services/users';

const UserItem = ({ user, onUserUpdated }) => {
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState(user);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      await userService.updateUser(user.id, formData);
      setEditing(false);
      onUserUpdated();
    } catch (error) {
      console.error('Error al actualizar usuario:', error);
      alert('Error al actualizar usuario');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`¿Estás seguro de eliminar al usuario ${user.username}?`)) {
      try {
        setLoading(true);
        await userService.deleteUser(user.id);
        onUserUpdated();
      } catch (error) {
        console.error('Error al eliminar usuario:', error);
        alert('Error al eliminar usuario');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleCancel = () => {
    setFormData(user);
    setEditing(false);
  };

  if (editing) {
    return (
      <tr>
        <td>{user.username}</td>
        <td>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
          />
        </td>
        <td>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
        </td>
        <td>{user.rol_nombre}</td>
        <td>
          <select 
            name="is_active" 
            value={formData.is_active}
            onChange={handleChange}
          >
            <option value={true}>Activo</option>
            <option value={false}>Inactivo</option>
          </select>
        </td>
        <td>
          <button onClick={handleSave} disabled={loading}>
            Guardar
          </button>
          <button onClick={handleCancel} disabled={loading}>
            Cancelar
          </button>
        </td>
      </tr>
    );
  }

  return (
    <tr>
      <td>{user.username}</td>
      <td>{user.first_name} {user.last_name}</td>
      <td>{user.email}</td>
      <td>{user.rol_nombre}</td>
      <td>{user.is_active ? 'Activo' : 'Inactivo'}</td>
      <td>
        <button onClick={() => setEditing(true)}>Editar</button>
        <button onClick={handleDelete} className="delete-button">
          Eliminar
        </button>
      </td>
    </tr>
  );
};

export default UserItem;