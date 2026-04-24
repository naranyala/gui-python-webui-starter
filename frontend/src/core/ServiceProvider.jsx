import React, { createContext, useContext, useMemo } from 'react';
import { initializeServices, resolve, SERVICE_KEYS } from './index.js';

// Create the Context
const ServiceContext = createContext(null);

/**
 * ServiceProvider provides a single source of truth for services.
 * It integrates with the core DI container.
 */
export function ServiceProvider({ children }) {
  const services = useMemo(() => {
    // Initialize the core DI container
    initializeServices();
    
    // We return a proxy that allows useService to resolve via the core container
    return {
      resolve: (key) => resolve(key)
    };
  }, []);

  return (
    <ServiceContext.Provider value={services}>
      {children}
    </ServiceContext.Provider>
  );
}

/**
 * useService is the frontend equivalent of backend's container.resolve()
 * It retrieves a service instance from the Core DI system.
 */
export function useService(ServiceClass) {
  const context = useContext(ServiceContext);
  if (!context) {
    throw new Error('useService must be used within a ServiceProvider');
  }
  
  // 1. If it's already a key from SERVICE_KEYS, use it
  if (typeof ServiceClass === 'symbol') {
    return context.resolve(ServiceClass);
  }

  // 2. Map Class Name to SERVICE_KEY
  const className = ServiceClass.name;
  const key = Object.entries(SERVICE_KEYS).find(([k, v]) => k.endsWith('_SERVICE') && k.startsWith(className.toUpperCase()))?.[1];

  if (key) {
    return context.resolve(key);
  }

  // 3. Fallback to resolving by class name directly
  try {
    return context.resolve(className);
  } catch (e) {
    console.error(`[useService] Failed to resolve service for: ${className}`, e);
    throw e;
  }
}
