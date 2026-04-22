from typing import Optional, List
import uuid
import logging
from .base import BaseService
from shared.types import Document
from shared.utils import format_timestamp
from ..core.database import get_db

logger = logging.getLogger(__name__)

class DocumentService(BaseService):
    """Service for managing documents via SQLite."""
    
    def __init__(self, container):
        super().__init__(container)
        self._db = get_db()
    
    def on_initialize(self) -> None:
        self._db.connect()
        logger.info("DocumentService initialized with SQLite")
    
    def get_all(self) -> List[Document]:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content, created_at, updated_at FROM documents")
        rows = cursor.fetchall()
        
        return [
            Document(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ) for row in rows
        ]
    
    def get_by_id(self, doc_id: str) -> Optional[Document]:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        
        if row:
            return Document(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
        return None
    
    def create(self, title: str, content: str) -> Document:
        doc_id = str(uuid.uuid4())[:8]
        now = format_timestamp()
        
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO documents (id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (doc_id, title, content, now, now)
        )
        conn.commit()
        
        return Document(id=doc_id, title=title, content=content, created_at=now, updated_at=now)
    
    def update(self, doc_id: str, title: str = None, content: str = None) -> Optional[Document]:
        doc = self.get_by_id(doc_id)
        if doc:
            now = format_timestamp()
            new_title = title if title else doc.title
            new_content = content if content else doc.content
            
            conn = self._db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE documents SET title = ?, content = ?, updated_at = ? WHERE id = ?",
                (new_title, new_content, now, doc_id)
            )
            conn.commit()
            
            doc.title = new_title
            doc.content = new_content
            doc.updated_at = now
        return doc
    
    def delete(self, doc_id: str) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        conn.commit()
        return cursor.rowcount > 0
