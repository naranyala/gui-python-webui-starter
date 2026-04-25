/**
 * Search Service - Handles document search
 */

import { BaseService } from './base.js';
import Fuse from 'fuse.js';

export class SearchService extends BaseService {
  constructor(container, apiClient) {
    super(container);
    this.apiClient = apiClient;
    this._fuse = null;
    this._documents = [];
    this._threshold = 0.4;
  }

  onInitialize() {
    this._fuse = new Fuse(this._documents, {
      keys: ['title', 'content'],
      threshold: this._threshold,
      includeScore: true,
      includeMatches: true,
    });
  }

  setDocuments(docs) {
    this._documents = docs;
    this._fuse = new Fuse(docs, {
      keys: ['title', 'content'],
      threshold: this._threshold,
      includeScore: true,
      includeMatches: true,
    });
  }

  setThreshold(threshold) {
    this._threshold = Math.max(0, Math.min(1, threshold));
    if (this._fuse) {
      this._fuse = new Fuse(this._documents, {
        keys: ['title', 'content'],
        threshold: this._threshold,
        includeScore: true,
        includeMatches: true,
      });
    }
  }

  async search(query, limit = 10) {
    if (!query || !this._fuse) {
      return [];
    }

    try {
      // Try API first
      const results = await this.apiClient.get('search', 'search', { q: query, limit });
      return results.map(r => ({
        item: { id: r.id, title: r.title },
        score: r.score,
      }));
    } catch (error) {
      console.warn('[SearchService] API unavailable, using local search');
    }

    // Fallback to local Fuse.js search
    const results = this._fuse.search(query, { limit });
    return results.map(r => ({
      item: r.item,
      score: 1 - r.score, // Convert similarity to score
      matches: r.matches,
    }));
  }

  searchLocal(query, limit = 10) {
    if (!query || !this._fuse) {
      return [];
    }

    const results = this._fuse.search(query, { limit });
    return results.map(r => ({
      item: r.item,
      score: 1 - r.score,
      matches: r.matches,
    }));
  }
}

export default SearchService;