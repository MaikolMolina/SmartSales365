import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Obtiene el contenedor principal
const container = document.getElementById('root');

// Crea la raíz moderna
const root = createRoot(container);

// Renderiza la aplicación
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
