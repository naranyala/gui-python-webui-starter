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
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._init_db()
    
    def _init_db(self):
        conn = cast(sqlite3.Connection, self.get_connection())
        cursor = conn.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, title TEXT, content TEXT, created_at TEXT, updated_at TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS todos (id TEXT PRIMARY KEY, task TEXT, completed INTEGER DEFAULT 0, created_at TEXT)")
        
        self._seed_docs_from_files()
        
        conn.commit()

    def _seed_docs_from_files(self):
        """Scan the /docs folder and seed the database with markdown files."""
        docs_dir = Path("docs")
        if not docs_dir.exists():
            logger.warning("Docs directory not found, skipping seeding")
            return

        now = format_timestamp()
        count = 0
        
        for md_file in docs_dir.glob("*.md"):
            doc_id = md_file.stem
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract title from first H1 or filename
                title = doc_id.replace('_', ' ').replace('-', ' ').title()
                if content.startswith('# '):
                    title = content.split('\n')[0].replace('# ', '').strip()
                
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM documents WHERE id = ?", (doc_id,))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO documents (id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                                 (doc_id, title, content, now, now))
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
