import api from './api';

export const aiService = {
  // CU12 - Entrenar modelo
  trainModel: async () => {
    try {
      const response = await api.post('/sales/api/train-model/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error de conexión' };
    }
  },

  // CU11 - Obtener predicciones
  getPredictions: async (days = 30) => {
    try {
      const response = await api.get(`/sales/api/get-predictions/?days=${days}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error de conexión' };
    }
  },

  // Estado del modelo
  getModelStatus: async () => {
    try {
      const response = await api.get('/sales/api/model-status/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error de conexión' };
    }
  }
};