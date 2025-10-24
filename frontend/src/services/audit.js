import api from './api';

export const auditService = {
  getAuditLogs: () => {
    return api.get('/auth/bitacora/').then(response => response.data);
  },

  getAuditLog: (id) => {
    return api.get(`/auth/bitacora/${id}/`).then(response => response.data);
  }
};