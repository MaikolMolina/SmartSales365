import api from './api';

export const roleService = {
  getRoles: () => {
    return api.get('/auth/roles/').then(response => response.data);
  },

  getRole: (id) => {
    return api.get(`/auth/roles/${id}/`).then(response => response.data);
  },

  createRole: (roleData) => {
    return api.post('/auth/roles/', roleData).then(response => response.data);
  },

  updateRole: (id, roleData) => {
    return api.put(`/auth/roles/${id}/`, roleData).then(response => response.data);
  },

  deleteRole: (id) => {
    return api.delete(`/auth/roles/${id}/`).then(response => response.data);
  }
};