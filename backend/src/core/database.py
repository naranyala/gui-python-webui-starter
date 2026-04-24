import sqlite3
import logging
from pathlib import Path
from typing import Optional, cast
from shared.utils import format_timestamp

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
    
    def connect(self):
        if self._conn is None:
            logger.info(f"Connecting to database: {self.db_path}")
            try:
                self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
                self._conn.row_factory = sqlite3.Row
                # Removed WAL mode to avoid potential filesystem I/O issues
                self._init_db()
            except sqlite3.Error as e:
                logger.error(f"Database connection error: {e}")
                raise e
    
    def _init_db(self):
        # Use the already established connection to avoid recursion
        conn = self._conn
        if conn is None:
            return
            
        cursor = conn.cursor()
        
        # For demo purposes, we drop and recreate to ensure a clean simplified structure
        tables = [
            "CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, title TEXT, content TEXT)",
            "CREATE TABLE IF NOT EXISTS todos (id TEXT PRIMARY KEY, task TEXT, completed INTEGER)",
            "CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, name TEXT, email TEXT)",
            "CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, name TEXT, status TEXT)",
            "CREATE TABLE IF NOT EXISTS logs (id TEXT PRIMARY KEY, level TEXT, message TEXT)",
            "CREATE TABLE IF NOT EXISTS settings (id TEXT PRIMARY KEY, key TEXT, value TEXT)",
        ]
        
        for sql in tables:
            cursor.execute(sql)
        
        self._seed_docs_from_files()
        self._seed_demo_data()
        
        conn.commit()

    def _seed_demo_data(self):
        # Use the already established connection
        conn = self._conn
        if conn is None:
            return
            
        cursor = conn.cursor()
        
        demo_data = {
            "users": [
                ('u1', 'Alice Smith', 'alice@example.com'),
                ('u2', 'Bob Jones', 'bob@example.com'),
                ('u3', 'Charlie Brown', 'charlie@example.com'),
            ],
            "projects": [
                ('p1', 'WebUI Starter', 'Active'),
                ('p2', 'Core Engine', 'In Progress'),
                ('p3', 'Auth Module', 'Pending'),
            ],
            "logs": [
                ('l1', 'INFO', 'System initialized'),
                ('l2', 'WARN', 'Low disk space'),
                ('l3', 'ERROR', 'Database connection lost'),
            ],
            "settings": [
                ('s1', 'theme', 'dark'),
                ('s2', 'notifications', 'enabled'),
                ('s3', 'auto_save', 'true'),
            ],
            "todos": [
                ('t1', 'Setup project', 1),
                ('t2', 'Implement CRUD', 0),
                ('t3', 'Write documentation', 0),
            ],
        }

        for table, rows in demo_data.items():
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            if cursor.fetchone()[0] == 0:
                cols = cursor.execute(f"PRAGMA table_info({table})").fetchall()
                col_names = [c['name'] for c in cols]
                placeholders = ", ".join(["?" for _ in col_names])
                sql = f"INSERT INTO {table} ({', '.join(col_names)}) VALUES ({placeholders})"
                cursor.executemany(sql, rows)
        
        conn.commit()


    def _seed_docs_from_files(self):
        """Scan the /docs folder and seed the database with markdown files."""
        docs_dir = Path("docs")
        if not docs_dir.exists():
            logger.warning("Docs directory not found, skipping seeding")
            return

        now = format_timestamp()
        count = 0
        
        conn = self._conn
        if conn is None:
            return
            
        cursor = conn.cursor()
        for md_file in docs_dir.glob("*.md"):
            doc_id = md_file.stem
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract title from first H1 or filename
                title = doc_id.replace('_', ' ').replace('-', ' ').title()
                if content.startswith('# '):
                    title = content.split('\n')[0].replace('# ', '').strip()
                
                cursor.execute("SELECT id FROM documents WHERE id = ?", (doc_id,))
                if not cursor.fetchone():
                    # simplified structure: id, title, content
                    cursor.execute("INSERT INTO documents (id, title, content) VALUES (?, ?, ?)",
                                 (doc_id, title, content))
                    count += 1
            except Exception as e:
                logger.error(f"Failed to load doc file {md_file}: {e}")
        
        if count > 0:
            logger.info(f"Seeded {count} new documents from /docs folder")

    def get_connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self.connect()
        conn = self._conn
        if conn is None:
            raise RuntimeError("Database connection failed")
        return conn # type: ignore

    def get_tables_info(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        # Get all tables except internal sqlite tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        results = []
        for table in tables:
            table_name = table['name']
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            
            # Get a sample column name for description
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            col_names = [c['name'] for c in columns]
            
            results.append({
                'id': table_name,
                'title': table_name.replace('_', ' ').title(),
                'icon': '📊',
                'description': f"{count} records | Cols: {', '.join(col_names[:3])}{'...' if len(col_names)>3 else ''}"
            })
        return results

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


_db: Optional[Database] = None
def get_db(db_path: str = "app.db") -> Database:
    global _db
    if _db is None:
        _db = Database(db_path)
    return _db
