import { BaseService } from './base.js';

export class TableCrudService extends BaseService {
  constructor(container, apiClient) {
    super(container);
    this.apiClient = apiClient;
  }

  async getData(tableName) {
    return this.apiClient.get('db', 'get_table_data', { table: tableName });
  }

  async insert(tableName, data) {
    return this.apiClient.post('db', 'insert_record', { table: tableName, data });
  }

  async delete(tableName, rowId) {
    return this.apiClient.delete('db', 'delete_record', { table: tableName, id: rowId });
  }
}
