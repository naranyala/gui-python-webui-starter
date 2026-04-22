import sqlite3
import logging
import json
from pathlib import Path
from typing import Optional
from shared.utils import format_timestamp

logger = logging.getLogger(__name__)

DOCS = [
    {
        "id": "arch",
        "title": "Project Architecture",
        "content": """# System Architecture

This project uses a **Hybrid Desktop Architecture** combining a Python backend with a React-based frontend.

## Key Layers
1. **Host**: Python 3.13+ managed by `uv`.
2. **GUI Shell**: `webui2` (native window wrapper).
3. **Frontend**: React 19 bundled with **Rspack**.
4. **API Layer**: Dual-path communication (WebUI Bridge + FastAPI).
5. **Persistence**: SQLite with WAL mode enabled.

## Module System
The project is strictly modularized into `frontend/src/modules/` and `backend/src/api/modules/`. Each feature (Docs, Todos, etc.) is an isolated unit with its own UI and API logic."""
    },
    {
        "id": "comm",
        "title": "Communication Bridge",
        "content": """# Backend-Frontend Communication

This starter supports two parallel communication paths.

## 1. WebUI Bridge (Primary)
- Uses internal OS pipes (IPC).
- Zero network overhead.
- No firewall issues.
- Integrated via `window.webui.call()` and `window.bind()`.

## 2. FastAPI (REST/WS)
- Standard HTTP endpoints.
- Used for development in external browsers.
- Supports WebSockets for real-time push from Python to UI.

## The Hybrid Client
The `ApiClient` in `frontend/src/services/base.js` automatically toggles between these modes based on the environment."""
    },
    {
        "id": "be-core",
        "title": "Backend Abstraction",
        "content": """# Backend Core Logic

## Dependency Injection
We use a custom `DIContainer` in `backend/src/core/container.py`. 
- **Singletons**: Services like `Database` and `DocumentService`.
- **Factories**: For transient object creation.

## Service Layer
Services extend `BaseService` and manage business logic and data access. They are initialized once during `main.py` startup.

## Database
SQLite is used for local persistence. We enable **WAL (Write-Ahead Logging)** to support concurrent access from the GUI and background API threads without locking errors."""
    },
    {
        "id": "fe-core",
        "title": "Frontend Abstraction",
        "content": """# Frontend Core Logic

## React Modules
Each feature lives in `frontend/src/modules/`. 
- **Page Components**: Entry point for the feature.
- **Service Hooks**: Bridging services to the UI.

## Observer Pattern
To prevent infinite re-renders and handle async Python calls, we use the **Observer Pattern**.
1. Services maintain the "Source of Truth".
2. Components `subscribe()` to service updates.
3. Services `_notify()` all subscribers when Python data returns.

## Reactivity
The project uses standard React primitives (`useState`, `useMemo`) for maximum compatibility and simplicity."""
    }
]

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
        cursor = self._conn.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, title TEXT, content TEXT, created_at TEXT, updated_at TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS todos (id TEXT PRIMARY KEY, task TEXT, completed INTEGER DEFAULT 0, created_at TEXT)")
        
        # Seed Technical Docs
        now = format_timestamp()
        for doc in DOCS:
            cursor.execute("SELECT id FROM documents WHERE id = ?", (doc['id'],))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO documents (id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                             (doc['id'], doc['title'], doc['content'], now, now))
        
        self._conn.commit()

    def get_connection(self) -> sqlite3.Connection:
        if self._conn is None: self.connect()
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

_db: Optional[Database] = None
def get_db(db_path: str = "app.db") -> Database:
    global _db
    if _db is None: _db = Database(db_path)
    return _db
