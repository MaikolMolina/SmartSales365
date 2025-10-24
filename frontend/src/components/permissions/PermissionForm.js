import React, { useState } from 'react';
import { permissionService } from '../../services/permissions';

const PermissionForm = ({ onPermissionCreated }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    codigo: '',
    descripcion: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await permissionService.createPermission(formData);
      onPermissionCreated();
      // Resetear formulario
      setFormData({
        nombre: '',
        codigo: '',
        descripcion: ''
      });
      alert('Permiso creado exitosamente');
    } catch (err) {
      console.error('Error al crear permiso:', err);
      setError('Error al crear permiso');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="permission-form">
      <h3>Crear Nuevo Permiso</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
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
            <label>Código:</label>
            <input
              type="text"
              name="codigo"
              value={formData.codigo}
              onChange={handleChange}
              required
            />
          </div>
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

        {error && <div className="error-message">{error}</div>}

        <button type="submit" disabled={loading} className="submit-button">
          {loading ? 'Creando...' : 'Crear Permiso'}
        </button>
      </form>
    </div>
  );
};

export default PermissionForm;
