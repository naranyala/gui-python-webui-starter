import { register, resolve, has, clear } from './container.js';
import { getConfig } from './config.js';
import { 
  ApiClient, 
  DocumentService, 
  SearchService, 
  GraphService,
  TodoService,
  NotificationService,
  DatabaseService
} from '../services/index.js';

// Service keys (use Symbols for private services)
export const SERVICE_KEYS = {
  T_SERVICE: Symbol.for('TableCrudService'),
  DOCUMENT_SERVICE: Symbol.for('DocumentService'),
  SEARCH_SERVICE: Symbol.for('SearchService'),
  GRAPH_SERVICE: Symbol.for('GraphService'),
  TODO_SERVICE: Symbol.for('TodoService'),
  DATABASE_SERVICE: Symbol.for('DatabaseService'),
  API_CLIENT: Symbol.for('ApiClient'),
  NOTIFICATION_SERVICE: Symbol.for('NotificationService'),
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

  // Register Notification service
  register(SERVICE_KEYS.NOTIFICATION_SERVICE, (container) => {
    return new NotificationService(container);
  });

  // Register services with DI
  register(SERVICE_KEYS.DOCUMENT_SERVICE, (container) => {
    return new DocumentService(container, container.resolve(SERVICE_KEYS.API_CLIENT));
  });

  register(SERVICE_KEYS.SEARCH_SERVICE, (container) => {
    return new SearchService(container, container.resolve(SERVICE_KEYS.API_CLIENT));
  });

  register(SERVICE_KEYS.GRAPH_SERVICE, (container) => {
    return new GraphService(container, container.resolve(SERVICE_KEYS.API_CLIENT));
  });

  register(SERVICE_KEYS.TODO_SERVICE, (container) => {
    return new TodoService(container, container.resolve(SERVICE_KEYS.API_CLIENT));
  });

  register(SERVICE_KEYS.DATABASE_SERVICE, (container) => {
    return new DatabaseService(container, container.resolve(SERVICE_KEYS.API_CLIENT));
  });

  register(SERVICE_KEYS.T_SERVICE, (container) => {
    return new TableCrudService(container, container.resolve(SERVICE_KEYS.API_CLIENT));
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
