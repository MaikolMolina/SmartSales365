import api from './api';

export const reportService = {
  // CU6 - Generar reporte por texto
  generateTextReport: async (prompt, format = 'JSON') => {
    const response = await api.post(
      '/reports/text-report/',
      { prompt, formato: format },
      {
        responseType:
          format === 'EXCEL' || format === 'PDF' ? 'blob' : 'json',
      }
    );
    return response;
  },
  // CU7 - Generar reporte por voz
  generateVoiceReport: async (audioBlob, format = 'JSON') => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.wav');
    formData.append('formato', format);

    const response = await api.post('/reports/voice-report/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response;
  },

  // Obtener historial de reportes
  getReportHistory: async () => {
    const response = await api.get('/reports/report-history/');
    return response.data;
  },

  // Descargar archivo
  downloadFile: (fileData, filename, contentType) => {
    const blob = new Blob([fileData], { type: contentType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }
};