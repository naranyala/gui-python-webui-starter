from typing import Optional
from ..core.container import get_container
from ..services import DocumentService, SearchService, GraphService, TodoService, SystemService, SettingsService
from ..api.dependencies import success_response, error_response

class ApiRoutes:
    """API route handlers."""
    
    def __init__(self):
        self._doc_service: Optional[DocumentService] = None
        self._search_service: Optional[SearchService] = None
        self._graph_service: Optional[GraphService] = None
        self._todo_service: Optional[TodoService] = None
        self._system_service: Optional[SystemService] = None
        self._settings_service: Optional[SettingsService] = None
    
    def _get_services(self):
        container = get_container()
        self._doc_service = container.resolve(DocumentService)
        self._search_service = container.resolve(SearchService)
        self._graph_service = container.resolve(GraphService)
        self._todo_service = container.resolve(TodoService)
        self._system_service = container.resolve(SystemService)
        self._settings_service = container.resolve(SettingsService)
    
    # Document routes
    def get_documents(self):
        self._get_services()
        docs = self._doc_service.get_all()
        return success_response([{"id": d.id, "title": d.title} for d in docs])
    
    def get_document(self, doc_id: str):
        self._get_services()
        doc = self._doc_service.get_by_id(doc_id)
        if not doc:
            return error_response(f"Document {doc_id} not found")
        return success_response({
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "created_at": doc.created_at,
            "updated_at": doc.updated_at,
        })
    
    def create_document(self, title: str, content: str):
        self._get_services()
        doc = self._doc_service.create(title, content)
        return success_response({"id": doc.id}, "Document created")
    
    def update_document(self, doc_id: str, title: str = None, content: str = None):
        self._get_services()
        doc = self._doc_service.update(doc_id, title, content)
        if not doc:
            return error_response(f"Document {doc_id} not found")
        return success_response({"id": doc.id}, "Document updated")
    
    def delete_document(self, doc_id: str):
        self._get_services()
        if self._doc_service.delete(doc_id):
            return success_response(None, "Document deleted")
        return error_response(f"Document {doc_id} not found")
    
    # Search routes
    def search_documents(self, query: str):
        self._get_services()
        docs = self._doc_service.get_all()
        results = self._search_service.search(query, docs)
        return success_response([
            {
                "id": r.item.id,
                "title": r.item.title,
                "score": r.score,
            }
            for r in results
        ])
    
    # Graph routes
    def get_graph(self):
        self._get_services()
        graph = self._graph_service.get_graph()
        if not graph:
            return error_response("Graph not initialized")
        return success_response({
            "nodes": [{"id": n.id, "label": n.label, "data": n.data} for n in graph.nodes],
            "edges": [{"id": e.id, "source": e.source, "target": e.target, "data": e.data} for e in graph.edges],
        })
    
    def add_graph_node(self, id: str, label: str):
        self._get_services()
        node = self._graph_service.add_node(id, label)
        return success_response({"id": node.id}, "Node added")
    
    def add_graph_edge(self, id: str, source: str, target: str):
        self._get_services()
        edge = self._graph_service.add_edge(id, source, target)
        if not edge:
            return error_response("Failed to add edge - nodes may not exist")
        return success_response({"id": edge.id}, "Edge added")

    # System routes
    def get_system_stats(self):
        self._get_services()
        return success_response(self._system_service.get_stats())

    # Settings routes
    def get_settings(self):
        self._get_services()
        return success_response(self._settings_service.get_all())
    
    def update_setting(self, key: str, value: Any):
        self._get_services()
        if self._settings_service.set_setting(key, value):
            return success_response(None, "Setting updated")
        return error_response("Failed to update setting")

# Singleton instance
_api_routes = ApiRoutes()

def get_api_routes() -> ApiRoutes:
    return _api_routes

__all__ = ['ApiRoutes', 'get_api_routes']