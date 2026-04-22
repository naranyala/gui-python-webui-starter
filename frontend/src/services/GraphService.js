/**
 * Graph Service - Handles graph data operations
 */

import { BaseService } from './base.js';

export class GraphService extends BaseService {
  constructor(container) {
    super(container);
    this._graphData = {
      nodes: [],
      edges: [],
    };
  }

  onInitialize() {
    // Initialize with sample graph
    this._graphData = {
      nodes: [
        { data: { id: 'a', label: 'Node A' } },
        { data: { id: 'b', label: 'Node B' } },
        { data: { id: 'c', label: 'Node C' } },
        { data: { id: 'd', label: 'Node D' } },
        { data: { id: 'e', label: 'Node E' } },
      ],
      edges: [
        { data: { id: 'e1', source: 'a', target: 'b' } },
        { data: { id: 'e2', source: 'b', target: 'c' } },
        { data: { id: 'e3', source: 'c', target: 'a' } },
        { data: { id: 'e4', source: 'd', target: 'c' } },
        { data: { id: 'e5', source: 'e', target: 'd' } },
      ],
    };
  }

  async getGraph() {
    try {
      const apiClient = this.container.resolve(Symbol.for('ApiClient'));
      const response = await apiClient.get('/graph');
      if (response.success && response.data) {
        this._graphData = {
          nodes: response.data.nodes.map(n => ({ data: n })),
          edges: response.data.edges.map(e => ({ data: e })),
        };
      }
    } catch (error) {
      console.warn('[GraphService] API unavailable, using local data');
    }
    return this._graphData;
  }

  getLocalGraph() {
    return this._graphData;
  }

  addNode(id, label, data = {}) {
    const node = { data: { id, label, ...data } };
    this._graphData.nodes.push(node);
    return node;
  }

  addEdge(id, source, target, data = {}) {
    // Verify nodes exist
    const nodeIds = new Set(this._graphData.nodes.map(n => n.data.id));
    if (!nodeIds.has(source) || !nodeIds.has(target)) {
      console.error('[GraphService] Cannot add edge: nodes not found');
      return null;
    }

    const edge = { data: { id, source, target, ...data } };
    this._graphData.edges.push(edge);
    return edge;
  }

  removeNode(nodeId) {
    this._graphData.nodes = this._graphData.nodes.filter(n => n.data.id !== nodeId);
    this._graphData.edges = this._graphData.edges.filter(
      e => e.data.source !== nodeId && e.data.target !== nodeId
    );
  }

  removeEdge(edgeId) {
    this._graphData.edges = this._graphData.edges.filter(e => e.data.id !== edgeId);
  }

  clear() {
    this._graphData.nodes = [];
    this._graphData.edges = [];
  }

  setGraph(nodes, edges) {
    this._graphData = { nodes, edges };
  }
}

export default GraphService;