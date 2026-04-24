import { describe, expect, it, mock, beforeEach } from "bun:test";
import { ApiClient } from "./base.js";

describe("ApiClient (BridgeClient)", () => {
  let client;
  let mockContainer = {
    resolve: mock()
  };

  beforeEach(() => {
    client = new ApiClient(mockContainer);
    
    // Mock window.webui.call
    global.window = {
      webui: {
        call: mock()
      }
    };
  });

  it("should format module:action correctly", async () => {
    const mockResponse = JSON.stringify({
      success: true,
      data: { items: [1, 2, 3] }
    });
    
    window.webui.call.mockResolvedValue(mockResponse);

    const result = await client.call('docs', 'get_all', { filter: 'all' });

    expect(window.webui.call).toHaveBeenCalledWith('docs:get_all', { filter: 'all' });
    expect(result).toEqual({ items: [1, 2, 3] });
  });

  it("should handle backend errors via success flag", async () => {
    const mockErrorResponse = JSON.stringify({
      success: false,
      error: 'Permission denied'
    });
    
    window.webui.call.mockResolvedValue(mockErrorResponse);

    await expect(client.call('sys', 'delete_root')).rejects.toThrow('Permission denied');
  });

  it("should use the same bridge call for all HTTP verb helpers", async () => {
    window.webui.call.mockResolvedValue(JSON.stringify({ success: true, data: {} }));
    
    await client.get('docs', 'list');
    expect(window.webui.call).toHaveBeenCalledWith('docs:list', undefined);
    
    await client.post('todos', 'add', { text: 'hi' });
    expect(window.webui.call).toHaveBeenCalledWith('todos:add', { text: 'hi' });
    
    await client.delete('files', 'remove', 'id123');
    expect(window.webui.call).toHaveBeenCalledWith('files:remove', 'id123');
  });
});
