import { describe, expect, it, mock, beforeEach } from "bun:test";
import { DocumentService } from "./DocumentService.js";

describe("DocumentService", () => {
  let service;
  let mockApiClient;
  let mockContainer;

  beforeEach(() => {
    mockApiClient = {
      get: mock(() => Promise.resolve({ success: true, data: [] })),
      post: mock(() => Promise.resolve({ success: true, data: {} })),
      put: mock(() => Promise.resolve({ success: true, data: {} })),
      delete: mock(() => Promise.resolve({ success: true })),
    };

    mockContainer = {
      resolve: mock((key) => {
        if (key === Symbol.for('ApiClient')) return mockApiClient;
        return null;
      }),
    };

    service = new DocumentService(mockContainer);
  });

  it("should initialize with sample documents", () => {
    service.initialize();
    const docs = service.getLocalDocuments();
    expect(docs.length).toBe(3);
    expect(docs[0].title).toBe("Getting Started");
  });

  it("should fetch all documents from API", async () => {
    const apiDocs = [{ id: '101', title: 'API Doc', content: '...' }];
    mockApiClient.get.mockImplementation(() => 
      Promise.resolve({ success: true, data: apiDocs })
    );

    const docs = await service.getAll();
    expect(mockApiClient.get).toHaveBeenCalledWith('/documents');
    expect(docs).toEqual(apiDocs);
  });

  it("should fallback to local data if API fails", async () => {
    service.initialize();
    mockApiClient.get.mockImplementation(() => 
      Promise.reject(new Error("Network error"))
    );

    const docs = await service.getAll();
    expect(docs.length).toBe(3);
  });

  it("should create a new document", async () => {
    const title = "New Doc";
    const content = "Content";
    
    const doc = await service.create(title, content);
    
    expect(doc.title).toBe(title);
    expect(mockApiClient.post).toHaveBeenCalled();
    expect(service.getLocalDocuments().length).toBe(1);
  });
});
