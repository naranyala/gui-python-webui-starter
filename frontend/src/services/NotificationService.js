import { BaseService } from './base.js';

/**
 * NotificationService for showing toast notifications
 * Uses a simple observer pattern so the UI can react to new notifications
 */
export class NotificationService extends BaseService {
  constructor(container) {
    super(container);
    this._notifications = [];
    this._subscribers = new Set();
  }

  subscribe(callback) {
    this._subscribers.add(callback);
    return () => this._subscribers.delete(callback);
  }

  _notify() {
    for (const callback of this._subscribers) {
      callback([...this._notifications]);
    }
  }

  notify(message, type = 'info', duration = 5000) {
    const id = Date.now();
    const notification = { id, message, type };
    
    this._notifications.push(notification);
    this._notify();

    setTimeout(() => {
      this.remove(id);
    }, duration);
    
    return id;
  }

  success(message, duration) {
    return this.notify(message, 'success', duration);
  }

  error(message, duration) {
    return this.notify(message, 'error', duration);
  }

  info(message, duration) {
    return this.notify(message, 'info', duration);
  }

  remove(id) {
    this._notifications = this._notifications.filter(n => n.id !== id);
    this._notify();
  }
}

export default NotificationService;
