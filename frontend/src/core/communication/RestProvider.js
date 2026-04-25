import CommunicationProvider from './Provider.js';
import { getConfig } from '../config.js';

/**
 * Standard REST Provider.
 * Uses HTTP POST requests to a backend API.
 */
export class RestProvider extends CommunicationProvider {
  async call(module, action, params) {
    const config = getConfig();
    const url = `${config.apiBase}/${module}/${action}`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ params })
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  }
}

export default RestProvider;
