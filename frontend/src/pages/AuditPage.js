import React, { useState } from 'react';
import AuditLog from '../components/audit/AuditLog';

const AuditPage = () => {
  const [refresh, setRefresh] = useState(false);

  const handleRefresh = () => {
    setRefresh(!refresh); // cambia el estado para recargar AuditLog
  };

  return (
    <div className="audit-page">
      <h1>Bitácora del Sistema</h1>
      <div className="page-content">
        {/* Aquí podrías agregar botones para refrescar manualmente */}
        <button onClick={handleRefresh}>Recargar Bitácora</button>

        <AuditLog refresh={refresh} />
      </div>
    </div>
  );
};

export default AuditPage;
