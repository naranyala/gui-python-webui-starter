/**
 * Shared types between frontend and backend
 */

/**
 * @typedef {Object} Document
 * @property {string} id
 * @property {string} title
 * @property {string} content
 * @property {string} [created_at]
 * @property {string} [updated_at]
 */

/**
 * @typedef {Object} GraphNode
 * @property {string} id
 * @property {string} label
 * @property {Object} [data]
 */

/**
 * @typedef {Object} GraphEdge
 * @property {string} id
 * @property {string} source
 * @property {string} target
 * @property {Object} [data]
 */

/**
 * @typedef {Object} GraphData
 * @property {GraphNode[]} nodes
 * @property {GraphEdge[]} edges
 */

/**
 * @typedef {Object} ApiResponse
 * @property {boolean} success
 * @property {*} [data]
 * @property {string} [error]
 * @property {string} [message]
 */

/**
 * @typedef {Object} SearchResult
 * @property {Document} item
 * @property {number} score
 * @property {Object[]} [matches]
 */

export const DocumentSchema = {
  id: { type: 'string', required: true },
  title: { type: 'string', required: true },
  content: { type: 'string', required: true },
  created_at: { type: 'string' },
  updated_at: { type: 'string' },
};

export const ApiResponseSchema = {
  success: { type: 'boolean', required: true },
  data: { type: 'any' },
  error: { type: 'string' },
  message: { type: 'string' },
};