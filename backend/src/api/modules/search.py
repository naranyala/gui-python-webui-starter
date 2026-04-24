import json
import logging
from typing import Any
from ...utils.response import format_response, api_handler

logger = logging.getLogger(__name__)

def setup_search_api(window, container):
    search_service = container.resolve("search_service")

    @api_handler
    def search_documents(e: Any):
        query = e.get_string()
        results = search_service.search(query)
        return [r.__dict__ if hasattr(r, '__dict__') else r for r in results]

    window.bind("search_documents", search_documents)
