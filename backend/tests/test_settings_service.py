import pytest
import sqlite3
import json
from backend.src.core.container import DIContainer
from backend.src.services import SettingsService
from backend.src.core.database import get_db

def test_settings_corruption_handling(tmp_path):
    """Test that the service handles non-JSON data in the settings table."""
    # Setup temp DB
    db_path = str(tmp_path / "test_settings.db")
    db = get_db(db_path)
    db.connect()
    
    # Manually insert corrupted (non-JSON) data
    conn = db.get_connection()
    conn.execute("CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT)")
    conn.execute("INSERT INTO settings (key, value) VALUES (?, ?)", ("theme", "NOT_JSON_DATA"))
    conn.commit()
    
    container = DIContainer()
    service = SettingsService(container)
    
    # This should not crash during initialization
    service.on_initialize()
    
    # The corrupted value should either be kept as string or handled gracefully
    # Depending on current implementation: it's kept as string if json.loads fails
    assert service.get_all().get("theme") == "NOT_JSON_DATA"

def test_settings_complex_types(tmp_path):
    """Test that nested dictionaries and lists are preserved through serialization."""
    db_path = str(tmp_path / "test_settings_complex.db")
    db = get_db(db_path)
    db.connect()
    
    container = DIContainer()
    service = SettingsService(container)
    service.on_initialize()
    
    complex_val = {"colors": ["red", "blue"], "timeout": 30, "enabled": True}
    service.set_setting("app.config", complex_val)
    
    # Reload from DB to verify
    service._settings = {} 
    service.on_initialize()
    
    assert service.get_all().get("app.config") == complex_val
