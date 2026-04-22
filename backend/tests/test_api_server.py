import pytest
from fastapi.testclient import TestClient
from backend.src.api.server import app
from backend.src.core.database import Database
from backend.src.core.container import get_container, DIContainer, set_container
from backend.src.services import DocumentService, TodoService

@pytest.fixture(autouse=True)
def setup_test_env(tmp_path):
    # Setup test container and database
    container = DIContainer()
    set_container(container)
    
    db_path = str(tmp_path / "test_api.db")
    from backend.src.core import database
    database._db = Database(db_path)
    
    container.register(DocumentService)
    container.register(TodoService)
    
    container.resolve(DocumentService).initialize()
    container.resolve(TodoService).initialize()
    
    yield
    
    database._db.close()
    database._db = None

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_docs_empty():
    response = client.get("/api/documents")
    assert response.status_code == 200
    # SQLite initializes with 1 doc by default in my database.py logic
    assert len(response.json()["data"]) >= 1

def test_todo_api_lifecycle():
    # 1. Create
    resp = client.post("/api/todos?task=API Task")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    todo_id = data["data"]["id"]
    
    # 2. Get all
    list_resp = client.get("/api/todos")
    assert any(t["id"] == todo_id for t in list_resp.json()["data"])

def test_concurrent_api_access():
    import threading
    
    results = []
    def call_api():
        try:
            resp = client.post("/api/todos?task=Concurrent Task")
            results.append(resp.status_code)
        except Exception:
            results.append(500)

    threads = [threading.Thread(target=call_api) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    assert all(r == 200 for r in results)
