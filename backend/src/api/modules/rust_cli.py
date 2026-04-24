import logging
from typing import Any
from ...utils.response import api_handler

logger = logging.getLogger(__name__)

def setup_rust_api(window, container):
    rust_service = container.resolve("rust_service")

    @api_handler
    def analyze_path(e: Any):
        path = e.get_string()
        # If path is empty, default to current directory
        if not path:
            path = "."
        return rust_service.analyze_directory(path)

    window.bind("analyze_path", analyze_path)
