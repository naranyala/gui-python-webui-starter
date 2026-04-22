import { describe, expect, it, mock, beforeEach, afterEach } from "bun:test";
import { ApiClient } from "./base.js";

describe("ApiClient", () => {
  let client;
  let mockContainer = {};

  beforeEach(() => {
    client = new ApiClient(mockContainer, "/test-api");
    // Mock global fetch
    global.fetch = mock(() => 
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ data: "ok" })
      })
    );
    // Ensure webui is not present for fetch tests
    delete window.webui;
  });

  it("should make a GET request with fetch", async () => {
    const response = await client.get("/docs");
    
    expect(global.fetch).toHaveBeenCalled();
    const [url, config] = global.fetch.mock.calls[0];
    expect(url).toBe("/test-api/docs");
    expect(response.data).toBe("ok");
  });

  it("should use webui.call if window.webui is present", async () => {
    window.webui = {
      call: mock(() => Promise.resolve(JSON.stringify({ test: "webui" })))
    };

    const response = await client.get("/documents");
    
    expect(window.webui.call).toHaveBeenCalledWith("get_documents", null);
    expect(response.data.test).toBe("webui");
  });
});
