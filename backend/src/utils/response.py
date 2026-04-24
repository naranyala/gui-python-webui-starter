import json
import logging
import traceback
from functools import wraps
from typing import Any, Optional, Callable

logger = logging.getLogger(__name__)

def format_response(success: bool, data: Any = None, error: Optional[str] = None, message: Optional[str] = None):
    return {
        "success": success,
        "data": data,
        "error": error,
        "message": message
    }

def api_handler(func: Callable):
    """Decorator to handle API function execution, logging, and error formatting."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # We expect the first arg to be 'window' if it's a binding, or 'e' (event)
        # The actual handler is usually defined inside setup_xxx_api
        # The function being decorated is the inner handler
        
        # Extract event data if available (for WebUI)
        event = args[0] if args else None
        event_info = ""
        if event is not None:
            try:
                # Try to get string representation of event if it's a webui event
                event_info = f" | Event: {event}"
            except:
                event_info = " | Event: <unreadable>"

        try:
            logger.info(f"[API Call] {func.__name__}{event_info}")
            result = func(*args, **kwargs)
            
            # If the result is already a JSON string, return it
            if isinstance(result, str):
                return result
            
            # If it's a dict, format it and return JSON
            if isinstance(result, dict):
                return json.dumps(result)
            
            # Otherwise, treat it as successful data
            return json.dumps(format_response(True, data=result))
            
        except Exception as e:
            error_msg = str(e)
            tb = traceback.format_exc()
            logger.error(f"[API Error] {func.__name__} failed: {error_msg}\n{tb}")
            return json.dumps(format_response(False, error=error_msg, message=f"An internal error occurred in {func.__name__}"))
            
    return wrapper
