from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# --- Document Models ---
class DocumentBase(BaseModel):
    title: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: str
    created_at: str
    updated_at: str

# --- Todo Models ---
class TodoBase(BaseModel):
    task: str

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: str
    completed: bool
    created_at: str

# --- System Models ---
class MemoryStats(BaseModel):
    total: int
    available: int
    used: int
    percent: float
    free: int

class DiskStats(BaseModel):
    total: int
    used: int
    free: int
    percent: float

class OSInfo(BaseModel):
    system: str
    release: str
    version: str
    machine: str

class SystemStatsResponse(BaseModel):
    cpu: float
    memory: MemoryStats
    disk: DiskStats
    os: OSInfo

# --- Settings Models ---
class SettingUpdate(BaseModel):
    key: str
    value: Any

# --- Graph Models ---
class GraphNode(BaseModel):
    id: str
    label: str
    data: Dict[str, Any] = Field(default_factory=dict)

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    data: Dict[str, Any] = Field(default_factory=dict)

class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

# --- Generic API Response ---
class ApiResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None
