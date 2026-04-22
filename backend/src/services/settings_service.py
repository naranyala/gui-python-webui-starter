import json
from typing import Any, Dict
from .base import BaseService
from ..core.database import get_db

class SettingsService(BaseService):
    """Service for managing application settings."""
    
    def __init__(self, container):
        super().__init__(container)
        self._settings: Dict[str, Any] = {}
    
    def on_initialize(self) -> None:
        self._load_settings()
    
    def _load_settings(self):
        db = get_db()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
        conn.commit()
        
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        for key, value in cursor.fetchall():
            try:
                self._settings[key] = json.loads(value)
            except json.JSONDecodeError:
                self._settings[key] = value
    
    def get_all(self) -> Dict[str, Any]:
        return self._settings
    
    def set_setting(self, key: str, value: Any):
        self._settings[key] = value
        db = get_db()
        conn = db.get_connection()
        serialized_value = json.dumps(value)
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
            (key, serialized_value)
        )
        conn.commit()
        return True
    
    def delete_setting(self, key: str):
        if key in self._settings:
            del self._settings[key]
            db = get_db()
            conn = db.get_connection()
            conn.execute("DELETE FROM settings WHERE key = ?", (key,))
            conn.commit()
            return True
        return False
