import React, { useEffect, useState } from 'react';
import { auditService } from '../../services/audit';

const AuditLog = ({ refresh }) => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadLogs = async () => {
    try {
      setLoading(true);
      const logsData = await auditService.getAuditLogs();
      setLogs(logsData);
    } catch (err) {
      setError('Error al cargar la bitácora');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
  }, [refresh]); // recarga cuando cambie refresh

  if (loading) return <div>Cargando bitácora...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Acción</th>
            <th>Modelo</th>
            <th>Descripción</th>
            <th>IP</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(log => (
            <tr key={log.id}>
              <td>{log.usuario_nombre}</td>
              <td>{log.accion}</td>
              <td>{log.modelo_afectado}</td>
              <td>{log.descripcion}</td>
              <td>{log.ip_address || '-'}</td>
              <td>{new Date(log.fecha_creacion).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AuditLog;
