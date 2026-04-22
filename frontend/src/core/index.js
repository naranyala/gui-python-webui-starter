import { register, resolve, has, clear } from './container.js';
import { getConfig } from './config.js';
import { 
  ApiClient, 
  DocumentService, 
  SearchService, 
  GraphService,
  TodoService
} from '../services/index.js';

// Service keys (use Symbols for private services)
export const SERVICE_KEYS = {
  DOCUMENT_SERVICE: Symbol.for('DocumentService'),
  SEARCH_SERVICE: Symbol.for('SearchService'),
  GRAPH_SERVICE: Symbol.for('GraphService'),
  TODO_SERVICE: Symbol.for('TodoService'),
  API_CLIENT: Symbol.for('ApiClient'),
  STORE: Symbol.for('Store'),
};

/**
 * Initialize the service container with all services
 */
export function initializeServices() {
  // Clear any existing registrations
  clear();

  const config = getConfig();

  // Register API client
  register(SERVICE_KEYS.API_CLIENT, (container) => {
    return new ApiClient(container, config.apiBase);
  });

  // Register services with DI
  register(SERVICE_KEYS.DOCUMENT_SERVICE, (container) => {
    return new DocumentService(container);
  });

  register(SERVICE_KEYS.SEARCH_SERVICE, (container) => {
    return new SearchService(container);
  });

  register(SERVICE_KEYS.GRAPH_SERVICE, (container) => {
    return new GraphService(container);
  });

  register(SERVICE_KEYS.TODO_SERVICE, (container) => {
    return new TodoService(container);
  });

  console.log('[Core] Services initialized');
}

/**
 * Get a service by key
 */
export function getService(key) {
  return resolve(key);
}

/**
 * Check if a service is available
 */
export function hasService(key) {
  return has(key);
}

/**
 * Re-export container utilities
 */
export { register, resolve, has, clear };

/**
 * Re-export config
 */
export { getConfig };
