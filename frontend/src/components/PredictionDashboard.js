import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Alert,
  Chip
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { aiService } from '../services/aiService';

const PredictionDashboard = () => {
  const [predictions, setPredictions] = useState([]);
  const [modelStatus, setModelStatus] = useState({ trained: false });
  const [loading, setLoading] = useState(false);
  const [training, setTraining] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    loadModelStatus();
    loadPredictions();
  }, []);

  const loadModelStatus = async () => {
    try {
      const status = await aiService.getModelStatus();
      setModelStatus(status);
    } catch (error) {
      console.error('Error loading model status:', error);
    }
  };

  const loadPredictions = async () => {
    setLoading(true);
    try {
      const result = await aiService.getPredictions(30);
      if (result.success) {
        setPredictions(result.predictions);
      } else {
        setMessage({ type: 'error', text: result.error });
      }
    } catch (error) {
      setMessage({ type: 'error', text: error.error || 'Error cargando predicciones' });
    } finally {
      setLoading(false);
    }
  };

  const handleTrainModel = async () => {
    setTraining(true);
    setMessage({ type: '', text: '' });
    
    try {
      const result = await aiService.trainModel();
      if (result.success) {
        setMessage({ 
          type: 'success', 
          text: `Modelo entrenado exitosamente! Precisión: ${(result.accuracy * 100).toFixed(2)}%` 
        });
        setModelStatus({ 
          trained: true, 
          accuracy: result.accuracy,
          last_training: new Date().toISOString()
        });
        loadPredictions();
      } else {
        setMessage({ type: 'error', text: result.error });
      }
    } catch (error) {
      setMessage({ type: 'error', text: error.error || 'Error entrenando modelo' });
    } finally {
      setTraining(false);
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'short'
    });
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard de Predicciones IA
      </Typography>

      {message.text && (
        <Alert severity={message.type || 'info'} sx={{ mb: 2 }}>
          {message.text}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Panel de estado del modelo */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Estado del Modelo
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Chip 
                  label={modelStatus.trained ? "Modelo Entrenado" : "Sin Entrenar"} 
                  color={modelStatus.trained ? "success" : "warning"}
                  variant="outlined"
                />
              </Box>

              {modelStatus.trained && (
                <>
                  <Typography variant="body2" color="textSecondary">
                    Último entrenamiento: {new Date(modelStatus.last_training).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Precisión: {modelStatus.accuracy ? (modelStatus.accuracy * 100).toFixed(2) + '%' : 'N/A'}
                  </Typography>
                </>
              )}

              <Button
                variant="contained"
                color="primary"
                onClick={handleTrainModel}
                disabled={training}
                fullWidth
                sx={{ mt: 2 }}
              >
                {training ? 'Entrenando Modelo...' : 'Entrenar Modelo (CU12)'}
              </Button>

              <Button
                variant="outlined"
                onClick={loadPredictions}
                disabled={loading}
                fullWidth
                sx={{ mt: 1 }}
              >
                Actualizar Predicciones
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Gráfico de predicciones */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Predicciones de Ventas - Próximos 30 Días (CU11)
            </Typography>
            
            {loading && <LinearProgress sx={{ mb: 2 }} />}
            
            {predictions.length > 0 ? (
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={predictions.map(p => ({
                  ...p,
                  date: formatDate(p.date),
                  sales: Math.round(p.sales)
                }))}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip formatter={(value) => [`$${value}`, 'Ventas Predichas']} />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="sales" 
                    stroke="#8884d8" 
                    strokeWidth={2}
                    name="Ventas Predichas"
                    dot={{ fill: '#8884d8' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Typography color="textSecondary">
                  {loading ? 'Cargando predicciones...' : 'No hay predicciones disponibles. Entrene el modelo primero.'}
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Estadísticas */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Estadísticas de Predicciones
              </Typography>
              {predictions.length > 0 && (
                <Grid container spacing={2}>
                  <Grid item xs={6} md={3}>
                    <Typography variant="body2" color="textSecondary">
                      Total Predicciones
                    </Typography>
                    <Typography variant="h6">
                      {predictions.length}
                    </Typography>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Typography variant="body2" color="textSecondary">
                      Ventas Promedio
                    </Typography>
                    <Typography variant="h6">
                      ${Math.round(predictions.reduce((sum, p) => sum + p.sales, 0) / predictions.length)}
                    </Typography>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Typography variant="body2" color="textSecondary">
                      Máxima Predicción
                    </Typography>
                    <Typography variant="h6">
                      ${Math.round(Math.max(...predictions.map(p => p.sales)))}
                    </Typography>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Typography variant="body2" color="textSecondary">
                      Mínima Predicción
                    </Typography>
                    <Typography variant="h6">
                      ${Math.round(Math.min(...predictions.map(p => p.sales)))}
                    </Typography>
                  </Grid>
                </Grid>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PredictionDashboard;