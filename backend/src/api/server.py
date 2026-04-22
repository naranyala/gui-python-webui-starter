import uvicorn
import json
import logging
import socket
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread

from ..core.container import get_container
from ..services import DocumentService, TodoService, GraphService, SystemService, SettingsService
from ..utils.response import format_response

logger = logging.getLogger(__name__)
app = FastAPI(title="WebUI Starter API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/documents")
async def get_docs():
    service = get_container().resolve(DocumentService)
    docs = service.get_all()
    return format_response(True, [d.__dict__ for d in docs])

@app.get("/api/todos")
async def get_todos():
    service = get_container().resolve(TodoService)
    return format_response(True, service.get_all())

@app.get("/api/graph")
async def get_graph():
    service = get_container().resolve(GraphService)
    graph = service.get_graph()
    if not graph:
        return format_response(False, None, "Graph not initialized")
    return format_response(True, {
        "nodes": [n.__dict__ for n in graph.nodes],
        "edges": [e.__dict__ for e in graph.edges],
    })

@app.get("/api/system")
async def get_system():
    service = get_container().resolve(SystemService)
    return format_response(True, service.get_stats())

@app.get("/api/settings")
async def get_settings():
    service = get_container().resolve(SettingsService)
    return format_response(True, service.get_all())

@app.post("/api/settings")
async def update_setting(payload: dict):
    service = get_container().resolve(SettingsService)
    key = payload.get('key')
    value = payload.get('value')
    if not key:
        return format_response(False, None, "Missing key")
    service.set_setting(key, value)
    return format_response(True, None, "Setting updated")

@app.post("/api/todos")
async def create_todo(task: str):
    service = get_container().resolve(TodoService)
    return format_response(True, service.create(task))

# WebSocket for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_text(json.dumps({
            "type": "status", 
            "message": "Backend Connected"
        }))
        while True:
            await websocket.receive_text()
    except Exception:
        pass

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def start_api_server(port=8000):
    """Run FastAPI in a background thread with port fallback."""
    current_port = port
    while is_port_in_use(current_port):
        logger.warning(f"Port {current_port} is in use, trying {current_port + 1}")
        current_port += 1
    
    def run():
        uvicorn.run(app, host="127.0.0.1", port=current_port, log_level="error")
    
    thread = Thread(target=run, daemon=True)
    thread.start()
    return current_port
