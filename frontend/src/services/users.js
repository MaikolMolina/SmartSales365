import api from './api';

export const userService = {
  getUsers: () => {
    return api.get('/auth/usuarios/').then(response => response.data);
  },

  getUser: (id) => {
    return api.get(`/auth/usuarios/${id}/`).then(response => response.data);
  },

  createUser: (userData) => {
    return api.post('/auth/usuarios/', userData).then(response => response.data);
  },

  updateUser: (id, userData) => {
    return api.put(`/auth/usuarios/${id}/`, userData).then(response => response.data);
  },

  deleteUser: (id) => {
    return api.delete(`/auth/usuarios/${id}/`).then(response => response.data);
  }
};