import CommunicationProvider from './Provider.js';

/**
 * WebUI Direct Provider.
 * Uses the 'module:action' direct binding.
 */
export class WebUIProvider extends CommunicationProvider {
  async call(module, action, params) {
    const cmd = `${module}:${action}`;
    if (!window.webui) {
      throw new Error('WebUI bridge not available');
    }
    const result = await window.webui.call(cmd, params);
    return JSON.parse(result);
  }
}

export default WebUIProvider;
