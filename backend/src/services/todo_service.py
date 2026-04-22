from typing import List, Optional
import uuid
import logging
from .base import BaseService
from ..core.database import get_db
from shared.utils import format_timestamp

logger = logging.getLogger(__name__)

class TodoService(BaseService):
    """Service for managing todos via SQLite (TodoMVC compatible)."""
    
    def __init__(self, container):
        super().__init__(container)
        self._db = get_db()
    
    def on_initialize(self) -> None:
        self._db.connect()
        logger.info("TodoService initialized")
    
    def get_all(self) -> List[dict]:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, completed, created_at FROM todos ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def create(self, task: str) -> dict:
        todo_id = str(uuid.uuid4())[:8]
        now = format_timestamp()
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (id, task, completed, created_at) VALUES (?, ?, ?, ?)",
            (todo_id, task, 0, now)
        )
        conn.commit()
        return {"id": todo_id, "task": task, "completed": 0, "created_at": now}
    
    def toggle(self, todo_id: str) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET completed = NOT completed WHERE id = ?", (todo_id,))
        conn.commit()
        return cursor.rowcount > 0

    def update_task(self, todo_id: str, task: str) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET task = ? WHERE id = ?", (task, todo_id))
        conn.commit()
        return cursor.rowcount > 0

    def delete(self, todo_id: str) -> bool:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        return cursor.rowcount > 0

    def clear_completed(self) -> int:
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE completed = 1")
        conn.commit()
        return cursor.rowcount
