/**
 * Frontend Dependency Injection Container
 * Implements a simple service locator pattern for dependency injection
 */

const container = new Map();
const singletons = new Map();

/**
 * Register a service in the container
 * @param {string|Symbol} key - Service identifier
 * @param {Function} factory - Factory function that receives the container
 * @param {boolean} singleton - Whether to return same instance (default: true)
 */
export function register(key, factory, singleton = true) {
  container.set(key, { factory, singleton, instance: null });
}

const containerProxy = {
  resolve: (key) => resolve(key),
  register: (key, factory, singleton) => register(key, factory, singleton),
  has: (key) => has(key)
};

/**
 * Resolve a service from the container
 * @param {string|Symbol} key - Service identifier
 * @returns {any} The resolved service instance
 */
export function resolve(key) {
  if (!container.has(key)) {
    throw new Error(`Service "${key.toString()}" not registered`);
  }

  const entry = container.get(key);

  if (entry.singleton) {
    if (!entry.instance) {
      entry.instance = entry.factory(containerProxy);
    }
    return entry.instance;
  }

  return entry.factory(containerProxy);
}

/**
 * Check if a service is registered
 * @param {string|Symbol} key - Service identifier
 * @returns {boolean}
 */
export function has(key) {
  return container.has(key);
}

/**
 * Clear all registered services (useful for testing)
 */
export function clear() {
  container.clear();
  singletons.clear();
}

/**
 * Create a new container scope
 * @returns {object} New container with register/resolve/has/clear
 */
export function createContainer() {
  const localContainer = new Map();
  const localSingletons = new Map();

  return {
    register: (key, factory, singleton = true) => {
      localContainer.set(key, { factory, singleton, instance: null });
      return localContainer.get(key);
    },
    resolve: (key) => {
      if (!localContainer.has(key)) {
        throw new Error(`Service "${key.toString()}" not registered`);
      }
      const entry = localContainer.get(key);
      if (entry.singleton) {
        if (!entry.instance) {
          entry.instance = entry.factory(localContainer.get.bind(localContainer));
        }
        return entry.instance;
      }
      return entry.factory(localContainer.get.bind(localContainer));
    },
    has: (key) => localContainer.has(key),
    clear: () => {
      localContainer.clear();
      localSingletons.clear();
    }
  };
}

export default { register, resolve, has, clear, createContainer };