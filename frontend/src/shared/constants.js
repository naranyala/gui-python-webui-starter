/**
 * Shared constants between frontend and backend
 */

export const APP_TITLE = 'DocViewer Demo';
export const APP_VERSION = '1.0.0';

// API paths
export const API_BASE_PATH = '/api';
export const API_DOCS_PATH = `${API_BASE_PATH}/documents`;
export const API_GRAPH_PATH = `${API_BASE_PATH}/graph`;
export const API_SEARCH_PATH = `${API_BASE_PATH}/search`;

// Search settings
export const SEARCH_THRESHOLD = 0.4;
export const SEARCH_LIMIT = 10;

// Graph settings
export const GRAPH_LAYOUT_DEFAULT = 'cose';
export const GRAPH_NODE_SIZE = 50;
export const GRAPH_EDGE_WIDTH = 2;

// Window settings
export const DEFAULT_WINDOW_WIDTH = 1200;
export const DEFAULT_WINDOW_HEIGHT = 800;

export const MODULES = [
  { id: 'docs', title: 'Documentation', icon: '📄', description: 'View and search markdown documents' },
  { id: 'graph', title: 'Interactive Graph', icon: '🕸️', description: 'Explore relationships in a graph view' },
  { id: 'system', title: 'System Monitor', icon: '🖥️', description: 'Real-time CPU and memory usage' },
  { id: 'settings', title: 'App Settings', icon: '⚙️', description: 'Configure application preferences' },
  { id: 'todos', title: 'Todo List', icon: '✅', description: 'Simple SQLite-backed task manager' },
];

// Event names
export const EVENTS = {
  DOCUMENT_SELECTED: 'document:selected',
  DOCUMENT_CREATED: 'document:created',
  DOCUMENT_UPDATED: 'document:updated',
  DOCUMENT_DELETED: 'document:deleted',
  GRAPH_UPDATED: 'graph:updated',
  SEARCH_PERFORMED: 'search:performed',
  TAB_CHANGED: 'tab:changed',
};

export default {
  APP_TITLE,
  APP_VERSION,
  API_BASE_PATH,
  API_DOCS_PATH,
  API_GRAPH_PATH,
  API_SEARCH_PATH,
  SEARCH_THRESHOLD,
  SEARCH_LIMIT,
  GRAPH_LAYOUT_DEFAULT,
  GRAPH_NODE_SIZE,
  GRAPH_EDGE_WIDTH,
  DEFAULT_WINDOW_WIDTH,
  DEFAULT_WINDOW_HEIGHT,
  EVENTS,
  MODULES,
};
