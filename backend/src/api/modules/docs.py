import logging
from typing import Any
from ...core.bridge import get_bridge

logger = logging.getLogger(__name__)

def setup_docs_api(window, container):
    bridge = get_bridge()
    doc_service = container.resolve("docs_service")

    def get_documents(arg: Any):
        docs = doc_service.get_all()
        return [d.__dict__ for d in docs]

    def get_document_by_id(arg: Any):
        doc_id = arg
        doc = doc_service.get_by_id(doc_id)
        return doc.__dict__ if doc else None

    bridge.bind("docs", "get_all", get_documents)
    bridge.bind("docs", "get_by_id", get_document_by_id)
