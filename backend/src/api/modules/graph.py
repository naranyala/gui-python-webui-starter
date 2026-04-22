import json
import logging
from typing import Any
from ...services import GraphService
from ...utils.response import format_response

logger = logging.getLogger(__name__)

def setup_graph_api(window, container):
    graph_service = container.resolve(GraphService)

    def get_graph(e: Any):
        try:
            graph = graph_service.get_graph()
            if not graph:
                return json.dumps(format_response(False, error="Graph not initialized"))
            
            data = {
                "nodes": [n.__dict__ for n in graph.nodes],
                "edges": [e.__dict__ for e in graph.edges],
            }
            return json.dumps(format_response(True, data))
        except Exception as ex:
            logger.error(f"Error in get_graph: {ex}")
            return json.dumps(format_response(False, error=str(ex)))

    window.bind("get_graph", get_graph)
