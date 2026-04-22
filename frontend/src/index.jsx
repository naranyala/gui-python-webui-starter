/**
 * Application Entry Point
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import { initializeServices } from './core/index.js';

// 1. Initialize services ONCE at the global level before React starts.
// This ensures that the DI container is stable and never cleared 
// during component re-renders or hot-reloads.
console.log('[Entry] Initializing global services...');
initializeServices();

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Debug helper
window.addEventListener('load', () => {
    if (window.webui) {
        console.log("[Entry] WebUI Bridge detected.");
    }
});
