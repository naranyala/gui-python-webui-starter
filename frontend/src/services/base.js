import { getConfig } from '../core/config.js';
import { z } from 'zod';

/**
 * Custom Error class for API failures
 */
export class ApiError extends Error {
  constructor(message, error = null, data = null) {
    super(message);
    this.name = 'ApiError';
    this.error = error;
    this.data = data;
  }
}

/**
 * Base Service class with DI support
 */
export class BaseService {
  constructor(container) {
    this.container = container;
    this._initialized = false;
  }

  initialize() {
    if (!this._initialized) {
      this.onInitialize();
      this._initialized = true;
    }
  }

  onInitialize() {
    // Override in subclass
  }

  ensureInitialized() {
    if (!this._initialized) {
      throw new Error(`${this.constructor.name} not initialized`);
    }
  }
}

/**
 * Bridge Client for symmetrical Frontend-Backend communication.
 * Calls are made using the 'module:action' pattern.
 */
export class ApiClient extends BaseService {
  constructor(container) {
    super(container);
  }

  /**
   * The core communication method.
   * @param {string} module - The backend module name (e.g., 'docs', 'todos')
   * @param {string} action - The action to perform (e.g., 'get_all', 'create')
   * @param {any} params - Arguments to pass to the backend
   */
  async call(module, action, params = null) {
    const cmd = `${module}:${action}`;
    console.log(`%c[Bridge Call] ${cmd}`, 'color: #3b82f6; font-weight: bold', { params });

    if (window.webui) {
      try {
        const result = await window.webui.call(cmd, params);
        const data = JSON.parse(result);
        
        if (!data.success) {
          const error = new ApiError(data.error || 'Bridge request failed');
          this._notifyError(error);
          console.error(`%c[Bridge Error] ${cmd}: ${data.error}`, 'color: #ef4444');
          throw error;
        }
        
        return data.data;
      } catch (error) {
        if (!(error instanceof ApiError)) {
          this._notifyError(error);
        }
        console.error(`%c[Bridge Exception] ${cmd}:`, 'color: #ef4444', error);
        throw error;
      }
    } else {
      // Fallback to REST if window.webui is not available
      return this._fallbackRest(module, action, params);
    }
  }

  async _fallbackRest(module, action, params) {
    const config = getConfig();
    const url = `${config.apiBase}/${module}/${action}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ params })
    });
    const data = await response.json();
    if (!data.success) throw new Error(data.error);
    return data.data;
  }

  _notifyError(error) {
    try {
      const notificationService = this.container.resolve(Symbol.for('NotificationService'));
      if (notificationService) {
        const message = error instanceof ApiError ? error.message : error.message || 'An unexpected error occurred';
        notificationService.error(message);
      }
    } catch (e) {
      // Notification service might not be registered yet
    }
  }

  // Convenience wrappers for common patterns
  get(module, action, params) { return this.call(module, action, params); }
  post(module, action, params) { return this.call(module, action, params); }
  put(module, action, params) { return this.call(module, action, params); }
  delete(module, action, params) { return this.call(module, action, params); }
}

export default { BaseService, ApiClient };
