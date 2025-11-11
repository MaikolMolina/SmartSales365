import React, { useState, useRef } from 'react';
import { reportService } from '../../services/reports';

const VoiceReport = ({ onReportGenerated, loading, setLoading }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [format, setFormat] = useState('JSON');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        await processAudio(audioBlob);
        
        // Detener stream
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setTranscript('Grabando... Habla ahora.');
    } catch (error) {
      onReportGenerated({
        type: 'error',
        message: 'Error accediendo al micrófono: ' + error.message
      });
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const processAudio = async (audioBlob) => {
    setLoading(true);
    try {
      const response = await reportService.generateVoiceReport(audioBlob, format);
      
      if (format === 'PDF' || format === 'EXCEL') {
        const filename = `reporte_voz_${Date.now()}.${format.toLowerCase()}`;
        const contentType = format === 'PDF' 
          ? 'application/pdf' 
          : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
        
        reportService.downloadFile(response.data, filename, contentType);
        onReportGenerated({
          type: 'download',
          message: `Reporte por voz descargado como ${format}`,
          format: format
        });
      } else {
        onReportGenerated({
          type: 'data',
          data: response.data,
          format: format
        });
        setTranscript(response.data.comando_interpretado?.original_command || 'Comando procesado');
      }
    } catch (error) {
      onReportGenerated({
        type: 'error',
        message: error.response?.data?.error || 'Error procesando audio'
      });
      setTranscript('Error: ' + (error.response?.data?.error || 'No se pudo procesar el audio'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="voice-report">
      <div className="voice-controls">
        <div className="format-selector">
          <label htmlFor="voice-format">Formato de salida:</label>
          <select 
            id="voice-format"
            value={format} 
            onChange={(e) => setFormat(e.target.value)}
            disabled={loading || isRecording}
          >
            <option value="JSON">Ver en pantalla</option>
            <option value="PDF">Descargar PDF</option>
            <option value="EXCEL">Descargar Excel</option>
          </select>
        </div>

        <div className="recording-section">
          {!isRecording ? (
            <button 
              onClick={startRecording}
              disabled={loading}
              className="record-button start"
            >
              🎤 Iniciar Grabación
            </button>
          ) : (
            <button 
              onClick={stopRecording}
              className="record-button stop"
            >
              ⏹️ Detener Grabación
            </button>
          )}

          <div className="recording-status">
            {isRecording && (
              <div className="pulsating-dot"></div>
            )}
            <span>{isRecording ? 'Grabando...' : 'Listo para grabar'}</span>
          </div>
        </div>

        {transcript && (
          <div className="transcript">
            <h4>Comando detectado:</h4>
            <p>{transcript}</p>
          </div>
        )}
      </div>

      <div className="voice-instructions">
        <h4>Instrucciones para comandos de voz:</h4>
        <ul>
          <li>Habla claro y pausadamente</li>
          <li>Incluye fechas específicas cuando sea necesario</li>
          <li>Menciona el formato deseado (PDF, Excel, o pantalla)</li>
          <li>Ejemplo: "Reporte de ventas de este mes en PDF"</li>
        </ul>
      </div>
    </div>
  );
};

export default VoiceReport;