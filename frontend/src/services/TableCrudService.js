import { BaseService } from './base.js';

export class TableCrudService extends BaseService {
  async getData(tableName) {
    return this.container.resolve(Symbol.for('ApiClient')).call('db', 'get_table_data', tableName);
  }

  async insert(tableName, data) {
    return this.container.resolve(Symbol.for('ApiClient')).call('db', 'insert_record', JSON.stringify({ table: tableName, data }));
  }

  async delete(tableName, rowId) {
    return this.container.resolve(Symbol.for('ApiClient')).call('db', 'delete_record', JSON.stringify({ table: tableName, id: rowId }));
  }
}
