import json
import logging
from typing import Any
from ...utils.response import format_response, api_handler

logger = logging.getLogger(__name__)

def setup_graph_api(window, container):
    graph_service = container.resolve("graph_service")

    @api_handler
    def get_graph(e: Any):
        graph = graph_service.get_graph()
        if not graph:
            # To trigger error in @api_handler, we can raise an exception
            # or the @api_handler could be modified to handle a specific Return value
            # Let's just raise a ValueError for now, as @api_handler catches it.
            raise ValueError("Graph not initialized")
        
        return {
            "nodes": [n.__dict__ for n in graph.nodes],
            "edges": [e.__dict__ for e in graph.edges],
        }

    window.bind("get_graph", get_graph)
