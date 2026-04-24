"""
Shared API constants to ensure symmetry between Frontend and Backend.
"""

# Module names used in the 'module:action' bridge pattern
class APIModules:
    DOCS = "docs"
    TODOS = "todos"
    SEARCH = "search"
    GRAPH = "graph"
    RUST = "rust"
    SYSTEM = "system"
    SETTINGS = "settings"
    CORE = "core"
