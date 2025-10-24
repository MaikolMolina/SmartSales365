import api, { setAuthToken } from './api';

export const authService = {
  login: async (username, password) => {
    const response = await api.post('/auth/login/', { username, password });
    const { user, token } = response.data;

    // Guardar token en localStorage
    localStorage.setItem('token', token);
    setAuthToken(token);

    return { user, token };
  },

  logout: async () => {
    await api.post('/auth/logout/');
    localStorage.removeItem('token');
    setAuthToken(null);
  },

  getCurrentUser: () => {
    const token = localStorage.getItem('token');
    if (!token) return null;
    setAuthToken(token);
    return {}; // opcional: guardar info del user en localStorage 
  }
};
