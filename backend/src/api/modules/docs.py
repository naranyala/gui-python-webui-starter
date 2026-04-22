import json
import logging
from typing import Any
from ...services import DocumentService
from ...utils.response import format_response

logger = logging.getLogger(__name__)

def setup_docs_api(window, container):
    doc_service = container.resolve(DocumentService)

    def get_documents(e: Any):
        try:
            docs = doc_service.get_all()
            data = [d.__dict__ for d in docs]
            return json.dumps(format_response(True, data))
        except Exception as ex:
            return json.dumps(format_response(False, error=str(ex)))

    def get_document_by_id(e: Any):
        try:
            doc_id = e.get_string()
            doc = doc_service.get_by_id(doc_id)
            data = doc.__dict__ if doc else None
            return json.dumps(format_response(True, data))
        except Exception as ex:
            return json.dumps(format_response(False, error=str(ex)))

    window.bind("get_documents", get_documents)
    window.bind("get_document_by_id", get_document_by_id)
