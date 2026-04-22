from typing import Optional
from ..core.container import get_container
from ..services import DocumentService, SearchService, GraphService, TodoService, SystemService, SettingsService
from ..api.dependencies import success_response, error_response
from .schemas import (
    DocumentCreate, DocumentUpdate, DocumentResponse,
    SystemStatsResponse,
    SettingUpdate,
    GraphResponse, GraphNode, GraphEdge
)

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
        if not self._doc_service:
            return error_response("Document service not initialized")
        docs = self._doc_service.get_all()
        return success_response([DocumentResponse(**d.__dict__) for d in docs])
    
    def get_document(self, doc_id: str):
        self._get_services()
        if not self._doc_service:
            return error_response("Document service not initialized")
        doc = self._doc_service.get_by_id(doc_id)
        if not doc:
            return error_response(f"Document {doc_id} not found")
        return success_response(DocumentResponse(**doc.__dict__))
    
    def create_document(self, data: dict):
        self._get_services()
        if not self._doc_service:
            return error_response("Document service not initialized")
        try:
            validated = DocumentCreate(**data)
            doc = self._doc_service.create(validated.title, validated.content)
            return success_response({"id": doc.id}, "Document created")
        except Exception as e:
            return error_response(f"Validation error: {str(e)}")
    
    def update_document(self, doc_id: str, data: dict):
        self._get_services()
        if not self._doc_service:
            return error_response("Document service not initialized")
        try:
            validated = DocumentUpdate(**data)
            doc = self._doc_service.update(
                doc_id, 
                title=validated.title, 
                content=validated.content
            )
            if not doc:
                return error_response(f"Document {doc_id} not found")
            return success_response({"id": doc.id}, "Document updated")
        except Exception as e:
            return error_response(f"Validation error: {str(e)}")
    
    def delete_document(self, doc_id: str):
        self._get_services()
        if not self._doc_service:
            return error_response("Document service not initialized")
        if self._doc_service.delete(doc_id):
            return success_response(None, "Document deleted")
        return error_response(f"Document {doc_id} not found")
    
    # Search routes
    def search_documents(self, query: str):
        self._get_services()
        if not self._doc_service or not self._search_service:
            return error_response("Required services not initialized")
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
        if not self._graph_service:
            return error_response("Graph service not initialized")
        graph = self._graph_service.get_graph()
        if not graph:
            return error_response("Graph not initialized")
        
        try:
            response = GraphResponse(
                nodes=[GraphNode(**n.__dict__) for n in graph.nodes],
                edges=[GraphEdge(**e.__dict__) for e in graph.edges]
            )
            return success_response(response.model_dump())
        except Exception as e:
            return error_response(f"Graph serialization error: {str(e)}")
    
    def add_graph_node(self, data: dict):
        self._get_services()
        if not self._graph_service:
            return error_response("Graph service not initialized")
        try:
            # Expecting { "id": "...", "label": "..." }
            node = self._graph_service.add_node(data['id'], data['label'])
            return success_response({"id": node.id}, "Node added")
        except KeyError as e:
            return error_response(f"Missing required field: {str(e)}")
    
    def add_graph_edge(self, data: dict):
        self._get_services()
        if not self._graph_service:
            return error_response("Graph service not initialized")
        try:
            # Expecting { "id": "...", "source": "...", "target": "..." }
            edge = self._graph_service.add_edge(data['id'], data['source'], data['target'])
            if not edge:
                return error_response("Failed to add edge - nodes may not exist")
            return success_response({"id": edge.id}, "Edge added")
        except KeyError as e:
            return error_response(f"Missing required field: {str(e)}")

    # System routes
    def get_system_stats(self):
        self._get_services()
        if not self._system_service:
            return error_response("System service not initialized")
        try:
            stats = self._system_service.get_stats()
            return success_response(SystemStatsResponse(**stats).model_dump())
        except Exception as e:
            return error_response(f"System stats error: {str(e)}")

    # Settings routes
    def get_settings(self):
        self._get_services()
        if not self._settings_service:
            return error_response("Settings service not initialized")
        return success_response(self._settings_service.get_all())
    
    def update_setting(self, data: dict):
        self._get_services()
        if not self._settings_service:
            return error_response("Settings service not initialized")
        try:
            validated = SettingUpdate(**data)
            if self._settings_service.set_setting(validated.key, validated.value):
                return success_response(None, "Setting updated")
            return error_response("Failed to update setting")
        except Exception as e:
            return error_response(f"Validation error: {str(e)}")

# Singleton instance
_api_routes = ApiRoutes()

def get_api_routes() -> ApiRoutes:
    return _api_routes

__all__ = ['ApiRoutes', 'get_api_routes']