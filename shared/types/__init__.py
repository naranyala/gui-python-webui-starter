from dataclasses import dataclass
from typing import Optional, Any, List, Dict

@dataclass
class Document:
    id: str
    title: str
    content: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class GraphNode:
    id: str
    label: str
    data: Optional[Dict[str, Any]] = None

@dataclass
class GraphEdge:
    id: str
    source: str
    target: str
    data: Optional[Dict[str, Any]] = None

@dataclass
class GraphData:
    nodes: List[GraphNode]
    edges: List[GraphEdge]

@dataclass
class ApiResponse:
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None

@dataclass
class SearchResult:
    item: Any
    score: float
    matches: Optional[List[Any]] = None