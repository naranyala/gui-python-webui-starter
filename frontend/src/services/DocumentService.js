/**
 * Document Service - Handles document operations
 */

import { BaseService } from './base.js';

export class DocumentService extends BaseService {
  constructor(container, apiClient) {
    super(container);
    this.apiClient = apiClient;
    this._documents = [];
  }

  onInitialize() {
    // Initialize with sample documents (fallback when API unavailable)
    this._documents = [
      {
        id: '1',
        title: 'Getting Started',
        content: `# Getting Started\n\nWelcome to **our app**!\n\n## Installation\n\n\`\`\`bash\nnpm install\nnpm run dev\n\`\`\`\n\n## Quick Start\n\nJust import and use:\n\n\`\`\`javascript\nimport { valtio } from 'valtio';\n\`\`\``,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        id: '2',
        title: 'API Reference',
        content: `# API Reference\n\n## Methods\n\n| Method | Description |\n|--------|-------------|\n| fetch() | Fetch data |\n| submit() | Submit form |\n\n\`\`\`typescript\ninterface User {\n  id: number;\n  name: string;\n}\n\`\`\``,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        id: '3',
        title: 'Graph Theory',
        content: `# Graph Theory\n\nA **graph** consists of vertices connected by edges.\n\n## Example\n\n$$E = mc^2$$\n\n> Graphs are everywhere!`,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ];
  }

  async getAll() {
    try {
      this._documents = await this.apiClient.get('docs', 'get_all');
    } catch (error) {
      console.warn('[DocumentService] API unavailable, using local data');
    }
    return this._documents;
  }

  async getById(id) {
    try {
      return await this.apiClient.get('docs', 'get_by_id', { doc_id: id });
    } catch (error) {
      // Fallback to local
    }
    return this._documents.find(d => d.id === id);
  }

  async create(title, content) {
    const newDoc = {
      id: String(Date.now()),
      title,
      content,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    try {
      await this.apiClient.post('docs', 'create', { title, content });
    } catch (error) {
      // Continue with local
    }

    this._documents.push(newDoc);
    return newDoc;
  }

  async update(id, title, content) {
    const doc = this._documents.find(d => d.id === id);
    if (doc) {
      doc.title = title ?? doc.title;
      doc.content = content ?? doc.content;
      doc.updated_at = new Date().toISOString();

      try {
        await this.apiClient.put('docs', 'update', { doc_id: id, title, content });
      } catch (error) {
        // Continue with local
      }
    }
    return doc;
  }

  async delete(id) {
    const index = this._documents.findIndex(d => d.id === id);
    if (index !== -1) {
      this._documents.splice(index, 1);
      try {
        await this.apiClient.delete('docs', 'delete', { doc_id: id });
      } catch (error) {
        // Continue with local
      }
      return true;
    }
    return false;
  }

  getLocalDocuments() {
    return this._documents;
  }
}

export default DocumentService;