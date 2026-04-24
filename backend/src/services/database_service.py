import logging
from typing import List, Dict, Any
from ..core.database import get_db
from ..core.bridge import api_action

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service for database introspection and generic table operations."""
    
    @api_action
    def get_tables(self, _=None) -> List[Dict[str, Any]]:
        """Returns a list of all user tables in the database."""
        db = get_db()
        tables_info = db.get_tables_info()
        return tables_info

    @api_action
    def get_table_data(self, table_name: str) -> List[Dict[str, Any]]:
        """Returns all data for a specific table."""
        db = get_db()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Validate table name
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            raise ValueError(f"Table {table_name} not found")
        
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    @api_action
    def insert_record(self, payload: str) -> Dict[str, Any]:
        """Inserts a record into a table. Payload is a JSON string: {'table': '...', 'data': {...}}"""
        import json
        try:
            params = json.loads(payload)
            table_name = params['table']
            data = params['data']
            
            db = get_db()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if not cursor.fetchone():
                raise ValueError(f"Table {table_name} not found")
            
            cols = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data])
            sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
            conn.commit()
            return {"id": cursor.lastrowid}
        except Exception as e:
            logger.error(f"Insert failed: {e}")
            raise e

    @api_action
    def delete_record(self, payload: str) -> Dict[str, Any]:
        """Deletes a record. Payload: {'table': '...', 'id': '...'}"""
        import json
        try:
            params = json.loads(payload)
            table_name = params['table']
            row_id = params['id']
            
            db = get_db()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if not cursor.fetchone():
                raise ValueError(f"Table {table_name} not found")
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            pk_col = next((c['name'] for c in columns if c['pk']), 'id')
            
            cursor.execute(f"DELETE FROM {table_name} WHERE {pk_col} = ?", (row_id,))
            conn.commit()
            return {"success": True}
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            raise e
