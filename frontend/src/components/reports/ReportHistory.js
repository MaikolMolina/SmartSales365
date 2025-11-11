import React, { useState, useEffect } from 'react';
import { reportService } from '../../services/reports';

const ReportHistory = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReportHistory();
  }, []);

  const loadReportHistory = async () => {
    try {
      const response = await reportService.getReportHistory();
      setReports(response.reportes || []);
    } catch (error) {
      console.error('Error cargando historial:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('es-ES');
  };

  const getFormatIcon = (format) => {
    switch (format) {
      case 'PDF': return '📄';
      case 'EXCEL': return '📊';
      default: return '👁️';
    }
  };

  if (loading) {
    return <div className="loading">Cargando historial...</div>;
  }

  return (
    <div className="report-history">
      <h3>Historial de Reportes</h3>
      
      {reports.length === 0 ? (
        <div className="empty-state">
          <p>No hay reportes generados aún</p>
        </div>
      ) : (
        <div className="reports-list">
          {reports.map((report) => (
            <div key={report.id} className="report-item">
              <div className="report-header">
                <span className="format-icon">
                  {getFormatIcon(report.formato)}
                </span>
                <span className="report-date">
                  {formatDate(report.fecha_creacion)}
                </span>
                <span className="report-stats">
                  {report.cantidad_resultados} resultados • {report.tiempo_ejecucion?.toFixed(2)}s
                </span>
              </div>
              
              <div className="report-prompt">
                {report.prompt}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ReportHistory;