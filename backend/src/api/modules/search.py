import json
import logging
from typing import Any
from ...services import SearchService
from ...utils.response import format_response

logger = logging.getLogger(__name__)

def setup_search_api(window, container):
    search_service = container.resolve(SearchService)

    def search_documents(e: Any):
        try:
            query = e.get_string()
            results = search_service.search(query)
            data = [r.__dict__ if hasattr(r, '__dict__') else r for r in results]
            return json.dumps(format_response(True, data))
        except Exception as ex:
            return json.dumps(format_response(False, error=str(ex)))

    window.bind("search_documents", search_documents)
