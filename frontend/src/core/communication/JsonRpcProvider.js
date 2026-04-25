import CommunicationProvider from './Provider.js';

/**
 * WebUI JSON-RPC Provider.
 * Uses the unified 'bridge:dispatch' entry point.
 */
export class JsonRpcProvider extends CommunicationProvider {
  async call(module, action, params) {
    if (!window.webui) {
      throw new Error('WebUI bridge not available');
    }
    
    const payload = {
      module,
      action,
      params
    };
    
    const result = await window.webui.call('bridge:dispatch', payload);
    return JSON.parse(result);
  }
}

export default JsonRpcProvider;
