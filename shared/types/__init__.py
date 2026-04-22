from dataclasses import dataclass
from typing import Optional

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
    data: Optional[dict] = None

@dataclass
class GraphEdge:
    id: str
    source: str
    target: str
    data: Optional[dict] = None

@dataclass
class GraphData:
    nodes: list[GraphNode]
    edges: list[GraphEdge]

@dataclass
class ApiResponse:
    success: bool
    data: Optional[any] = None
    error: Optional[str] = None
    message: Optional[str] = None

@dataclass
class SearchResult:
    item: any
    score: float
    matches: Optional[list] = None