import React, { createContext, useContext, useMemo } from 'react';
import { GraphService } from '../services/GraphService';
import { DocumentService } from '../services/DocumentService';
import { TodoService } from '../services/TodoService';
import { BaseService } from '../services/base';

// Create the Context
const ServiceContext = createContext(null);

/**
 * ServiceProvider provides a single source of truth for services.
 * It mimics the Backend DIContainer by instantiating services once
 * and making them available via React Context.
 */
export function ServiceProvider({ children }) {
  const services = useMemo(() => {
    // In a real app, we'd resolve these from a config or a registry
    // For now, we instantiate the core services.
    const container = {
        resolve: (key) => {
            // Minimal mock for internal service dependencies if needed
            return servicesMap[key];
        }
    };

    const servicesMap = {
      GraphService: new GraphService(container),
      DocumentService: new DocumentService(container),
      TodoService: new TodoService(container),
    };

    // Initialize all services
    Object.values(servicesMap).forEach(s => {
        if (s instanceof BaseService) s.initialize();
    });

    return servicesMap;
  }, []);

  return (
    <ServiceContext.Provider value={services}>
      {children}
    </ServiceContext.Provider>
  );
}

/**
 * useService is the frontend equivalent of backend's container.resolve()
 * It retrieves a service instance from the Context.
 */
export function useService(ServiceClass) {
  const services = useContext(ServiceContext);
  if (!services) {
    throw new Error('useService must be used within a ServiceProvider');
  }
  
  const service = services[ServiceClass.name];
  if (!service) {
    throw new Error(`Service ${ServiceClass.name} not found in ServiceProvider`);
  }
  
  return service;
}
