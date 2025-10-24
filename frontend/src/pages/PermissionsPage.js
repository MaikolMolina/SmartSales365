import React, { useState } from 'react';
import PermissionForm from '../components/permissions/PermissionForm';
import PermissionList from '../components/permissions/PermissionList';

const PermissionsPage = () => {
  const [refresh, setRefresh] = useState(false);

  const handlePermissionCreated = () => {
    setRefresh(!refresh);
  };

  return (
    <div className="permissions-page">
      <h1>Gestión de Permisos</h1>
      <div className="page-content">
        <div className="form-section">
          <PermissionForm onPermissionCreated={handlePermissionCreated} />
        </div>
        <div className="list-section">
          <PermissionList key={refresh} />
        </div>
      </div>
    </div>
  );
};

export default PermissionsPage;
