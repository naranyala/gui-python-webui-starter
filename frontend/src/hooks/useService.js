/**
 * Custom hook to use DI services in React components
 */

import { useContext, createContext } from 'react';
import { resolve, SERVICE_KEYS } from '../core/index.js';

// Create React context for services
const ServiceContext = createContext({});

/**
 * Provider component that makes services available
 */
export function ServiceProvider({ children, services = {} }) {
  return (
    <ServiceContext.Provider value={services}>
      {children}
    </ServiceContext.Provider>
  );
}

/**
 * Hook to get a service from the DI container
 * @param {Symbol} serviceKey - The service key to resolve
 * @returns {any} The service instance
 */
export function useService(serviceKey) {
  return resolve(serviceKey);
}

/**
 * Hook to get all services
 */
export function useServices() {
  return useContext(ServiceContext);
}

/**
 * Pre-defined hooks for common services
 */
export function useDocumentService() {
  return useService(SERVICE_KEYS.DOCUMENT_SERVICE);
}

export function useSearchService() {
  return useService(SERVICE_KEYS.SEARCH_SERVICE);
}

export function useGraphService() {
  return useService(SERVICE_KEYS.GRAPH_SERVICE);
}

export function useApiClient() {
  return useService(SERVICE_KEYS.API_CLIENT);
}

export default {
  ServiceProvider,
  useService,
  useServices,
  useDocumentService,
  useSearchService,
  useGraphService,
  useApiClient,
};