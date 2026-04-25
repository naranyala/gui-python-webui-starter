import { BaseService } from './base.js';

/**
 * TodoService with Observer Pattern
 * This ensures that multiple components can stay in sync
 * and prevents infinite re-rendering loops.
 */
export class TodoService extends BaseService {
  constructor(container, apiClient) {
    super(container);
    this.apiClient = apiClient;
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

  async getAll() {
    if (this._loading) return;
    
    this._loading = true;
    this._notify();
    
    try {
      this._todos = await this.apiClient.get('todos', 'get_all');
    } catch (error) {
      console.error('[TodoService] Failed to fetch todos', error);
    } finally {
      this._loading = false;
      this._notify();
    }
  }

  async create(task) {
    try {
      const todo = await this.apiClient.post('todos', 'create', { task });
      this._todos = [todo, ...this._todos];
      this._notify();
      return todo;
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
      await this.apiClient.put('todos', 'toggle', { todo_id: id });
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
      await this.apiClient.delete('todos', 'delete', { todo_id: id });
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
      await this.apiClient.delete('todos', 'clear_completed');
    } catch (error) {
      this._todos = original;
      this._notify();
    }
  }
}

export default TodoService;
