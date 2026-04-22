import { BaseService } from './base.js';

/**
 * TodoService with Observer Pattern
 * This ensures that multiple components can stay in sync
 * and prevents infinite re-rendering loops.
 */
export class TodoService extends BaseService {
  constructor(container) {
    super(container);
    this._todos = [];
    this._subscribers = new Set();
    this._loading = false;
  }

  // --- Observer Implementation ---
  subscribe(callback) {
    this._subscribers.add(callback);
    // Return unsubscribe function
    return () => this._subscribers.delete(callback);
  }

  _notify() {
    for (const callback of this._subscribers) {
      callback({
        todos: [...this._todos],
        loading: this._loading
      });
    }
  }

  // --- Data Actions ---
  async getAll() {
    if (this._loading) return;
    
    this._loading = true;
    this._notify();
    
    try {
      const response = await this.container.resolve(Symbol.for('ApiClient')).get('/todos');
      if (response.success && response.data) {
        this._todos = response.data;
      }
    } catch (error) {
      console.error('[TodoService] Failed to fetch todos', error);
    } finally {
      this._loading = false;
      this._notify();
    }
  }

  async create(task) {
    try {
      const response = await this.container.resolve(Symbol.for('ApiClient')).post('/todos', task);
      if (response.success && response.data) {
        this._todos = [response.data, ...this._todos];
        this._notify();
        return response.data;
      }
    } catch (error) {
      console.error('[TodoService] Failed to create todo', error);
    }
    return null;
  }

  async toggle(id) {
    // Optimistic Update
    const original = [...this._todos];
    this._todos = this._todos.map(t => 
      t.id === id ? { ...t, completed: t.completed ? 0 : 1 } : t
    );
    this._notify();

    try {
      const response = await this.container.resolve(Symbol.for('ApiClient')).put(`/todos/${id}/toggle`);
      if (!response.success) {
        this._todos = original;
        this._notify();
      }
    } catch (error) {
      this._todos = original;
      this._notify();
    }
  }

  async delete(id) {
    const original = [...this._todos];
    this._todos = this._todos.filter(t => t.id !== id);
    this._notify();

    try {
      const response = await this.container.resolve(Symbol.for('ApiClient')).delete(`/todos/${id}`);
      if (!response.success) {
        this._todos = original;
        this._notify();
      }
    } catch (error) {
      this._todos = original;
      this._notify();
    }
  }

  async clearCompleted() {
    const original = [...this._todos];
    this._todos = this._todos.filter(t => !t.completed);
    this._notify();

    try {
      const response = await this.container.resolve(Symbol.for('ApiClient')).delete('/todos/completed');
      if (!response.success) {
        this._todos = original;
        this._notify();
      }
    } catch (error) {
      this._todos = original;
      this._notify();
    }
  }
}

export default TodoService;
