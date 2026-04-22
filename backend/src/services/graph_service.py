from typing import Optional
from .base import BaseService
from shared.types import GraphData, GraphNode, GraphEdge

class GraphService(BaseService):
    """Service for managing graph data."""
    
    def __init__(self, container):
        super().__init__(container)
        self._graph_data: Optional[GraphData] = None
    
    def on_initialize(self) -> None:
        # Initialize with sample graph
        nodes = [
            GraphNode(id="a", label="Node A"),
            GraphNode(id="b", label="Node B"),
            GraphNode(id="c", label="Node C"),
            GraphNode(id="d", label="Node D"),
            GraphNode(id="e", label="Node E"),
        ]
        edges = [
            GraphEdge(id="e1", source="a", target="b"),
            GraphEdge(id="e2", source="b", target="c"),
            GraphEdge(id="e3", source="c", target="a"),
            GraphEdge(id="e4", source="d", target="c"),
            GraphEdge(id="e5", source="e", target="d"),
        ]
        self._graph_data = GraphData(nodes=nodes, edges=edges)
    
    def get_graph(self) -> Optional[GraphData]:
        return self._graph_data
    
    def add_node(self, id: str, label: str, data: dict = None) -> GraphNode:
        node = GraphNode(id=id, label=label, data=data)
        if self._graph_data:
            self._graph_data.nodes.append(node)
        return node
    
    def add_edge(self, id: str, source: str, target: str, data: dict = None) -> Optional[GraphEdge]:
        if not self._graph_data:
            return None
        
        # Verify nodes exist
        node_ids = {n.id for n in self._graph_data.nodes}
        if source not in node_ids or target not in node_ids:
            return None
        
        edge = GraphEdge(id=id, source=source, target=target, data=data)
        self._graph_data.edges.append(edge)
        return edge
    
    def remove_node(self, node_id: str) -> bool:
        if not self._graph_data:
            return False
        
        # Remove node
        self._graph_data.nodes = [n for n in self._graph_data.nodes if n.id != node_id]
        
        # Remove connected edges
        self._graph_data.edges = [
            e for e in self._graph_data.edges 
            if e.source != node_id and e.target != node_id
        ]
        return True
    
    def remove_edge(self, edge_id: str) -> bool:
        if not self._graph_data:
            return False
        
        self._graph_data.edges = [e for e in self._graph_data.edges if e.id != edge_id]
        return True
    
    def clear(self):
        if self._graph_data:
            self._graph_data.nodes.clear()
            self._graph_data.edges.clear()