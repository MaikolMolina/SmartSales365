import React, { useState } from 'react';
import UserList from '../components/users/UserList';
import UserForm from '../components/users/UserForm';

const UsersPage = () => {
  const [refresh, setRefresh] = useState(false);

  const handleUserCreated = () => {
    setRefresh(!refresh);
  };

  return (
    <div className="users-page">
      <h1>Gestión de Usuarios</h1>
      <div className="page-content">
        <div className="form-section">
          <UserForm onUserCreated={handleUserCreated} />
        </div>
        <div className="list-section">
          <UserList key={refresh} />
        </div>
      </div>
    </div>
  );
};

export default UsersPage;