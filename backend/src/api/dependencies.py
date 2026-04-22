from typing import Optional, Any
from dataclasses import dataclass
from shared.types import ApiResponse

@dataclass
class RequestContext:
    """Request context for API handlers."""
    request_id: str
    user_agent: Optional[str] = None

def create_response(data=None, success: bool = True, error: Optional[str] = None, message: Optional[str] = None) -> ApiResponse:
    """Helper to create API responses."""
    return ApiResponse(
        success=success,
        data=data,
        error=error,
        message=message
    )

def success_response(data, message: Optional[str] = None) -> ApiResponse:
    return create_response(data=data, success=True, message=message)

def error_response(error: str, message: Optional[str] = None) -> ApiResponse:
    return create_response(success=False, error=error, message=message)

__all__ = [
    'ApiResponse',
    'RequestContext',
    'create_response',
    'success_response',
    'error_response',
]