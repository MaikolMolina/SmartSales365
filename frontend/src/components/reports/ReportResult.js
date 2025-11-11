import React from 'react';

const ReportResult = ({ result, onClose }) => {
  if (!result) return null;

  const renderDataTable = (data) => {
    if (!data || data.length === 0) {
      return <p>No hay datos para mostrar</p>;
    }

    const headers = Object.keys(data[0]);

    return (
      <div className="data-table-container">
        <table className="data-table">
          <thead>
            <tr>
              {headers.map(header => (
                <th key={header}>{header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                {headers.map(header => (
                  <td key={header}>{row[header]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className={`report-result ${result.type}`}>
      <div className="result-header">
        <h3>
          {result.type === 'data' && '📊 Reporte Generado'}
          {result.type === 'download' && '✅ Descarga Completada'}
          {result.type === 'error' && '❌ Error'}
        </h3>
        <button onClick={onClose} className="close-button">✕</button>
      </div>

      <div className="result-content">
        {result.type === 'error' && (
          <div className="error-message">
            <p>{result.message}</p>
          </div>
        )}

        {result.type === 'download' && (
          <div className="download-message">
            <p>{result.message}</p>
          </div>
        )}

        {result.type === 'data' && result.data && (
          <div className="data-result">
            <div className="result-info">
              {result.data?.comando_interpretado && (
                <p><strong>Comando:</strong> {result.data.comando_interpretado.original_command}</p>
              )}
              {result.data?.tiempo_ejecucion != null && (
                <p><strong>Tiempo de ejecución:</strong> {result.data.tiempo_ejecucion.toFixed(2)} segundos</p>
              )}
              <p><strong>Resultados:</strong> {result.data.datos?.length || 0} registros</p>
            </div>

            {result.data.datos && renderDataTable(result.data.datos)}

            {result.data.consulta && (
              <details className="query-details">
                <summary>Ver consulta SQL generada</summary>
                <pre className="sql-query">{result.data.consulta}</pre>
              </details>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ReportResult;
