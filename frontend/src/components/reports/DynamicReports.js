import React, { useState } from 'react';
import TextReport from './TextReport';
import VoiceReport from './VoiceReport';
import ReportHistory from './ReportHistory';
import ReportResult from './ReportResult';
import './DynamicReports.css';

const DynamicReports = () => {
  const [activeTab, setActiveTab] = useState('text');
  const [reportResult, setReportResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleReportGenerated = (result) => {
    setReportResult(result);
  };

  const clearResult = () => {
    setReportResult(null);
  };

  return (
    <div className="dynamic-reports">
      <div className="reports-header">
        <h1>Reportes Dinámicos</h1>
        <p>Genera reportes usando comandos de texto o voz</p>
      </div>

      {reportResult && (
        <ReportResult 
          result={reportResult} 
          onClose={clearResult}
        />
      )}

      <div className="reports-tabs">
        <button 
          className={`tab-button ${activeTab === 'text' ? 'active' : ''}`}
          onClick={() => setActiveTab('text')}
        >
          📝 Reporte por Texto
        </button>
        <button 
          className={`tab-button ${activeTab === 'voice' ? 'active' : ''}`}
          onClick={() => setActiveTab('voice')}
        >
          🎤 Reporte por Voz
        </button>
        <button 
          className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          📊 Historial
        </button>
      </div>

      <div className="reports-content">
        {activeTab === 'text' && (
          <TextReport 
            onReportGenerated={handleReportGenerated}
            loading={loading}
            setLoading={setLoading}
          />
        )}
        
        {activeTab === 'voice' && (
          <VoiceReport 
            onReportGenerated={handleReportGenerated}
            loading={loading}
            setLoading={setLoading}
          />
        )}
        
        {activeTab === 'history' && (
          <ReportHistory />
        )}
      </div>
    </div>
  );
};

export default DynamicReports;