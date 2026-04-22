from typing import Any, Optional

def format_response(success: bool, data: Any = None, error: Optional[str] = None, message: Optional[str] = None):
    return {
        "success": success,
        "data": data,
        "error": error,
        "message": message
    }
