import { getConfig } from '../core/config.js';
import { z } from 'zod';

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
 * API Client for making HTTP or Bridge requests
 */
export class ApiClient extends BaseService {
  constructor(container) {
    super(container);
  }

  async requestWebUI(endpoint, options = {}) {
    console.log(`[ApiClient] WebUI Request: ${endpoint}`, options);
    
    // Map REST-like endpoints to WebUI function names
    const mapping = {
      '/documents': 'get_documents',
      '/documents/': 'get_document_by_id',
      'POST /documents': 'create_document',
      '/search': 'search_documents',
      '/todos': 'get_todos',
      '/graph': 'get_graph',
      '/system': 'get_system_stats',
      '/settings': 'get_settings',
      'POST /settings': 'update_setting',
      'POST /todos': 'create_todo',
      '/todos/': 'toggle_todo',
      'DELETE /todos/': 'delete_todo',
      'DELETE /todos/completed': 'clear_completed_todos',
    };

    try {
      let funcName = mapping[endpoint];
      let arg = null;

      // Handle search with query params
      if (endpoint.startsWith('/search')) {
          funcName = mapping['/search'];
          const url = new URL(endpoint, 'http://localhost');
          arg = url.searchParams.get('q');
      }

      // Handle ID in URL
      if (!funcName && endpoint.startsWith('/documents/')) {
          funcName = mapping['/documents/'];
          arg = endpoint.split('/').pop();
      }

      // Handle ID in URL for todos toggle and delete
      if (!funcName && endpoint.startsWith('/todos/')) {
          const parts = endpoint.split('/');
          if (parts.length === 4 && parts[3] === 'toggle') {
              funcName = mapping['/todos/'];
              arg = parts[2];
          } else {
              funcName = mapping['DELETE /todos/'];
              arg = parts[2];
          }
      }

      // Handle POST requests
      if (options.method === 'POST') {
          if (endpoint === '/documents') funcName = mapping['POST /documents'];
          if (endpoint === '/todos') funcName = mapping['POST /todos'];
          arg = options.body;
      }

      if (funcName) {
          const result = await window.webui.call(funcName, arg);
          return JSON.parse(result);
      }
      
      throw new Error(`Unmapped WebUI endpoint: ${endpoint}`);
    } catch (error) {
      console.error(`[ApiClient] WebUI call failed: ${endpoint}`, error);
      throw error;
    }
  }

  async request(endpoint, options = {}) {
    const config = getConfig();
    const mode = config.commMode;

    // Use WebUI Bridge if mode is BRIDGE and we are in WebUI
    if (mode === 'BRIDGE' && window.webui) {
      return this.requestWebUI(endpoint, options);
    }

    // Fallback to standard fetch (FastAPI/REST)
    const url = `${config.apiBase}${endpoint}`;
    const fetchConfig = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, fetchConfig);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      // Basic validation: Ensure we have a success flag
      if (typeof data !== 'object' || data === null || !('success' in data)) {
        throw new Error('Invalid API response format: missing "success" flag');
      }

      return data;
    } catch (error) {
      console.error(`[ApiClient] Request failed: ${endpoint}`, error);
      throw error;
    }
  }

  get(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString();
    const url = query ? `${endpoint}?${query}` : endpoint;
    return this.request(url);
  }

  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: typeof data === 'string' ? data : JSON.stringify(data),
    });
  }

  put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: typeof data === 'string' ? data : JSON.stringify(data),
    });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

export default { BaseService, ApiClient };
