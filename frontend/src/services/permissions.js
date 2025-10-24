import api from './api';

export const permissionService = {
  getPermissions: () => {
    return api.get('/auth/permisos/').then(response => response.data);
  },

  getPermission: (id) => {
    return api.get(`/auth/permisos/${id}/`).then(response => response.data);
  },

  createPermission: (permissionData) => {
    return api.post('/auth/permisos/', permissionData).then(response => response.data);
  },

  updatePermission: (id, permissionData) => {
    return api.put(`/auth/permisos/${id}/`, permissionData).then(response => response.data);
  },

  deletePermission: (id) => {
    return api.delete(`/auth/permisos/${id}/`).then(response => response.data);
  }
};