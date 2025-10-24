import React, { useState, useEffect } from 'react';
import { userService } from '../../services/users';
import UserItem from './UserItem';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const usersData = await userService.getUsers();
      setUsers(usersData);
    } catch (err) {
      setError('Error al cargar los usuarios');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUserUpdated = () => {
    loadUsers();
  };

  if (loading) return <div>Cargando usuarios...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="user-list">
      <h3>Lista de Usuarios</h3>
      {users.length === 0 ? (
        <p>No hay usuarios registrados</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Usuario</th>
                <th>Nombre</th>
                <th>Email</th>
                <th>Rol</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <UserItem 
                  key={user.id} 
                  user={user} 
                  onUserUpdated={handleUserUpdated}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default UserList;