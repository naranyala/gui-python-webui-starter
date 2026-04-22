import pytest
from backend.src.core.container import DIContainer
from backend.src.services import GraphService

def test_add_edge_missing_nodes():
    """Test that adding an edge to non-existent nodes fails gracefully."""
    container = DIContainer()
    service = GraphService(container)
    service.on_initialize()
    
    # Attempt to add edge where source 'z' doesn't exist
    result = service.add_edge("e_fail", "z", "a")
    assert result is None
    
    # Attempt to add edge where target 'z' doesn't exist
    result = service.add_edge("e_fail2", "a", "z")
    assert result is None

def test_circular_reference():
    """Test that circular references in the graph are handled correctly."""
    container = DIContainer()
    service = GraphService(container)
    service.on_initialize()
    
    # Create A -> B -> C -> A
    service.add_node("n1", "Node 1")
    service.add_node("n2", "Node 2")
    service.add_node("n3", "Node 3")
    
    service.add_edge("e1", "n1", "n2")
    service.add_edge("e2", "n2", "n3")
    service.add_edge("e3", "n3", "n1")
    
    graph = service.get_graph()
    # Check that all edges exist
    edge_ids = [e.id for e in graph.edges]
    assert "e1" in edge_ids
    assert "e2" in edge_ids
    assert "e3" in edge_ids

def test_node_deletion_cleanup():
    """Test that deleting a node removes all associated edges."""
    container = DIContainer()
    service = GraphService(container)
    service.on_initialize()
    
    # record edges BEFORE adding our test ones
    initial_edges_count = len(service.get_graph().edges)
    
    # Setup: Node A connected to B and C
    service.add_node("a", "A")
    service.add_node("b", "B")
    service.add_node("c", "C")
    service.add_edge("e1", "a", "b")
    service.add_edge("e2", "c", "a")
    
    # Delete node A
    service.remove_node("a")
    
    graph = service.get_graph()
    # Ensure no edges remain that point to or from 'a'
    for edge in graph.edges:
        assert edge.source != "a"
        assert edge.target != "a"
    
    # Edge count should return to initial count
    assert len(graph.edges) == initial_edges_count
