import React, { useState } from 'react';
import { reportService } from '../../services/reports';

const TextReport = ({ onReportGenerated, loading, setLoading }) => {
  const [prompt, setPrompt] = useState('');
  const [format, setFormat] = useState('JSON');
  const [examples] = useState([
    "Quiero un reporte de ventas del mes de septiembre, agrupado por producto, en PDF",
    "Muestra las ventas del periodo del 01/10/2024 al 01/01/2025 en Excel",
    "Reporte de productos más vendidos este año",
    "Clientes con más compras en el último mes agrupado por cliente"
  ]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    try {
      const response = await reportService.generateTextReport(prompt, format);
      
      if (format === 'PDF' || format === 'EXCEL') {
        const filename = format === 'EXCEL'
          ? `reporte_${Date.now()}.xlsx`  // fuerza .xlsx
          : `reporte_${Date.now()}.${format.toLowerCase()}`;
        
        const contentType = format === 'PDF' 
          ? 'application/pdf' 
          : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
        
        reportService.downloadFile(response.data, filename, contentType);
        onReportGenerated({
          type: 'download',
          message: `Reporte descargado como ${format}`,
          format: format
        });
      } else {
        onReportGenerated({
          type: 'data',
          data: response.data,
          format: format
        });
      }
    } catch (error) {
      onReportGenerated({
        type: 'error',
        message: error.response?.data?.error || 'Error generando reporte'
      });
    } finally {
      setLoading(false);
    }
  };

  // ✅ Función normal para aplicar un ejemplo
  const applyExample = (example) => {
    setPrompt(example);
  };

  return (
    <div className="text-report">
      <form onSubmit={handleSubmit} className="report-form">
        <div className="form-group">
          <label htmlFor="prompt">Describe el reporte que necesitas:</label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ej: Quiero un reporte de ventas del mes de septiembre, agrupado por producto, en PDF"
            rows="4"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="format">Formato de salida:</label>
          <select 
            id="format"
            value={format} 
            onChange={(e) => setFormat(e.target.value)}
            disabled={loading}
          >
            <option value="JSON">Ver en pantalla</option>
            <option value="PDF">Descargar PDF</option>
            <option value="EXCEL">Descargar Excel</option>
          </select>
        </div>

        <button 
          type="submit" 
          disabled={!prompt.trim() || loading}
          className="generate-button"
        >
          {loading ? 'Generando...' : 'Generar Reporte'}
        </button>
      </form>

      <div className="examples-section">
        <h4>Ejemplos de comandos:</h4>
        <div className="examples-grid">
          {examples.map((example, index) => (
            <div 
              key={index}
              className="example-card"
              onClick={() => applyExample(example)} // ✅ Aquí usamos la función normal
            >
              {example}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TextReport;
