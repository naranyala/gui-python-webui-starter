import WebUIProvider from './WebUIProvider.js';
import JsonRpcProvider from './JsonRpcProvider.js';
import RestProvider from './RestProvider.js';
import { getConfig } from '../config.js';

export function createCommunicationProvider() {
  const config = getConfig();
  const mode = config.commMode;

  console.log(`%c[Comm] Initializing communication provider: ${mode}`, 'color: #10b981; font-weight: bold');

  switch (mode) {
    case 'BRIDGE':
      return new WebUIProvider();
    case 'JSON_RPC':
      return new JsonRpcProvider();
    case 'REST':
      return new RestProvider();
    default:
      console.warn(`Unknown commMode "${mode}", falling back to BRIDGE`);
      return new WebUIProvider();
  }
}

export default createCommunicationProvider;
