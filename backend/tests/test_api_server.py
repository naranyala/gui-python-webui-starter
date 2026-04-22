import pytest
from fastapi.testclient import TestClient
from backend.src.api.server import app
from backend.src.core.database import Database
from backend.src.core.container import DIContainer, set_container
from backend.src.services import DocumentService, TodoService

@pytest.fixture(autouse=True)
def setup_test_env(tmp_path):
    # Setup test container and database
    container = DIContainer()
    set_container(container)
    
    db_path = str(tmp_path / "test_api.db")
    from backend.src.core import database
    database._db = Database(db_path)
    
    # Instantiate and register services
    from backend.src.services import DocumentService, TodoService, GraphService, SearchService, SystemService, SettingsService
    
    doc_s = DocumentService(container)
    todo_s = TodoService(container)
    graph_s = GraphService(container)
    search_s = SearchService(container)
    sys_s = SystemService(container)
    set_s = SettingsService(container)
    
    container.register(DocumentService, doc_s)
    container.register(TodoService, todo_s)
    container.register(GraphService, graph_s)
    container.register(SearchService, search_s)
    container.register(SystemService, sys_s)
    container.register(SettingsService, set_s)
    
    # Initialize them
    for s in [doc_s, todo_s, graph_s, search_s, sys_s, set_s]:
        s.initialize()
    
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
    import requests
    
    # Use the actual server port (assuming it's running or we use a test server)
    # For a true integration test, we'd use the TestClient in a way that supports threads
    # but TestClient is synchronous. We'll use a real requests call to a test server
    # or simulate it by calling the routes directly.
    
    results = []
    def call_api():
        try:
            # We call the route handler directly to avoid network overhead and port conflicts
            # and to test the underlying logic concurrency.
            from backend.src.api.routes import get_api_routes
            routes = get_api_routes()
            # Note: routes._get_services() handles the DI
            resp = routes.add_graph_node({"id": f"node_{threading.get_ident()}", "label": "test"})
            results.append(resp.success)
        except Exception:
            results.append(False)

    threads = [threading.Thread(target=call_api) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    assert all(r is True for r in results)
