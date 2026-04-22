import { describe, expect, it, mock, beforeEach } from "bun:test";
import { ApiClient } from "./base.js";

describe("Communication Resilience", () => {
  let client;

  beforeEach(() => {
    client = new ApiClient({});
    // Mock global fetch
    global.fetch = mock(() => Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ success: true, data: [] })
    }));
    // Clear webui
    delete window.webui;
  });

  it("should handle backend latency gracefully", async () => {
    // Mock a slow response
    global.fetch.mockImplementation(() => new Promise(resolve => 
      setTimeout(() => resolve({ 
        ok: true, 
        json: () => Promise.resolve({ success: true, data: "slow" }) 
      }), 50)
    ));
    
    const start = Date.now();
    const result = await client.get("/slow-api");
    expect(Date.now() - start).toBeGreaterThanOrEqual(50);
    expect(result.data).toBe("slow");
  });

  it("should throw on malformed JSON from WebUI Bridge", async () => {
    window.webui = {
      call: mock(() => Promise.resolve("INVALID_NON_JSON"))
    };

    try {
        await client.requestWebUI("/documents");
        expect(false).toBe(true); // Should not reach here
    } catch (e) {
        expect(e).toBeInstanceOf(SyntaxError);
    }
  });

  it("should handle network errors in REST mode", async () => {
    global.fetch.mockImplementation(() => Promise.reject(new Error("Network Down")));
    
    try {
        await client.get("/docs");
        expect(false).toBe(true);
    } catch (e) {
        expect(e.message).toBe("Network Down");
    }
  });
});
