import { BaseService } from './base.js';

export class DatabaseService extends BaseService {
  async getTables() {
    return this.container.resolve(Symbol.for('ApiClient')).call('db', 'get_tables');
  }
}
