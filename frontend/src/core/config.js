/**
 * Frontend Configuration
 */

export const config = {
  appName: 'DocViewer',
  appVersion: '1.0.0',
  
  // Communication mode: 'BRIDGE' (WebUI IPC) or 'REST' (FastAPI)
  commMode: 'BRIDGE',
  
  // API settings (FastAPI)
  apiBase: 'http://localhost:8000/api',
  wsBase: 'ws://localhost:8000/ws',
  
  // Search settings
  searchThreshold: 0.4,
  searchLimit: 10,
  
  // Feature flags
  features: {
    enableSearch: true,
    enableGraph: true,
    enableMarkdown: true,
  }
};

export function getConfig() {
  return config;
}

export function setConfig(newConfig) {
  Object.assign(config, newConfig);
}

export default config;
