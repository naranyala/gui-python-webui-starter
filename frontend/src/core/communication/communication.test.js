import { describe, it, expect, vi, beforeEach } from 'bun:test';
import { getConfig, setConfig } from '../../core/config.js';
import createCommunicationProvider from './index.js';
import WebUIProvider from './WebUIProvider.js';
import JsonRpcProvider from './JsonRpcProvider.js';
import RestProvider from './RestProvider.js';

describe('Communication Providers', () => {
  beforeEach(() => {
    // Reset mocks and global state
    vi.restoreAllMocks();
    
    // Setup mock window
    global.window = {
      webui: {
        call: vi.fn()
      }
    };
    
    // Setup mock fetch
    global.fetch = vi.fn();
  });

  describe('WebUIProvider (Direct Mode)', () => {
    it('should call window.webui.call with "module:action" format', async () => {
      const provider = new WebUIProvider();
      const mockResponse = JSON.stringify({ success: true, data: 'direct-ok' });
      window.webui.call.mockResolvedValue(mockResponse);

      const result = await provider.call('test', 'greet', { name: 'Bun' });

      expect(window.webui.call).toHaveBeenCalledWith('test:greet', { name: 'Bun' });
      expect(result).toEqual({ success: true, data: 'direct-ok' });
    });

    it('should throw error if window.webui is missing', async () => {
      delete window.webui;
      const provider = new WebUIProvider();
      await expect(provider.call('test', 'greet')).rejects.toThrow('WebUI bridge not available');
    });
  });

  describe('JsonRpcProvider (Dispatch Mode)', () => {
    it('should call window.webui.call with "bridge:dispatch" and structured payload', async () => {
      const provider = new JsonRpcProvider();
      const mockResponse = JSON.stringify({ success: true, data: 'rpc-ok' });
      window.webui.call.mockResolvedValue(mockResponse);

      const result = await provider.call('test', 'greet', { name: 'Bun' });

      expect(window.webui.call).toHaveBeenCalledWith('bridge:dispatch', {
        module: 'test',
        action: 'greet',
        params: { name: 'Bun' }
      });
      expect(result).toEqual({ success: true, data: 'rpc-ok' });
    });
  });

  describe('RestProvider (HTTP Mode)', () => {
    it('should make a POST request to the correct URL', async () => {
      setConfig({ apiBase: 'http://api.test' });
      const provider = new RestProvider();
      
      const mockResponse = {
        ok: true,
        json: async () => ({ success: true, data: 'rest-ok' })
      };
      global.fetch.mockResolvedValue(mockResponse);

      const result = await provider.call('test', 'greet', { name: 'Bun' });

      expect(global.fetch).toHaveBeenCalledWith('http://api.test/test/greet', expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ params: { name: 'Bun' } })
      }));
      expect(result).toEqual({ success: true, data: 'rest-ok' });
    });

    it('should throw error on non-ok response', async () => {
      setConfig({ apiBase: 'http://api.test' });
      const provider = new RestProvider();
      
      const mockResponse = {
        ok: false,
        status: 500,
        json: async () => ({ error: 'Internal Server Error' })
      };
      global.fetch.mockResolvedValue(mockResponse);

      await expect(provider.call('test', 'greet')).rejects.toThrow('Internal Server Error');
    });
  });

  describe('Communication Provider Factory', () => {
    it('should create WebUIProvider when mode is BRIDGE', () => {
      setConfig({ commMode: 'BRIDGE' });
      const provider = createCommunicationProvider();
      expect(provider).toBeInstanceOf(WebUIProvider);
    });

    it('should create JsonRpcProvider when mode is JSON_RPC', () => {
      setConfig({ commMode: 'JSON_RPC' });
      const provider = createCommunicationProvider();
      expect(provider).toBeInstanceOf(JsonRpcProvider);
    });

    it('should create RestProvider when mode is REST', () => {
      setConfig({ commMode: 'REST' });
      const provider = createCommunicationProvider();
      expect(provider).toBeInstanceOf(RestProvider);
    });

    it('should fallback to WebUIProvider for unknown mode', () => {
      setConfig({ commMode: 'UNKNOWN' });
      const provider = createCommunicationProvider();
      expect(provider).toBeInstanceOf(WebUIProvider);
    });
  });
});
