import React, { useState } from 'react';
import RoleList from '../components/roles/RoleList';
import RoleForm from '../components/roles/RoleForm';

const RolesPage = () => {
  const [refresh, setRefresh] = useState(false);

  const handleRoleCreated = () => {
    setRefresh(!refresh);
  };

  return (
    <div className="roles-page">
      <h1>Gestión de Roles</h1>
      <div className="page-content">
        <div className="form-section">
          <RoleForm onClose={() => {}} onSuccess={handleRoleCreated} />
        </div>
        <div className="list-section">
          <RoleList key={refresh} />
        </div>
      </div>
    </div>
  );
};

export default RolesPage;
