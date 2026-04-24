import logging
import json
import traceback
from functools import wraps
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)

def api_action(func):
    """Decorator to mark a method as a bridge-exposed API action."""
    func._is_api_action = True
    return func

class Bridge:
    """
    Central registry for Frontend-Backend communication.
    Enforces a 'module:action' naming convention and provides unified logging.
    """
    def __init__(self, window):
        self.window = window
        self.registry: Dict[str, Callable] = {}

    def bind(self, module: str, action: str, handler: Callable):
        """Registers a function under a module:action namespace."""
        cmd_name = f"{module}:{action}"
        
        @wraps(handler)
        def wrapper(event):
            # Extract argument from WebUI event
            arg = None
            if event:
                try:
                    arg = event.get_string()
                except:
                    arg = event

            logger.info(f"🚀 [Bridge Request] {cmd_name} | Arg: {arg}")
            
            try:
                # Execute the handler
                # If the handler is a method, we pass the arg. 
                # Note: the actual handler is already bound to the service instance
                result = handler(arg)
                
                # Standardize the response
                response = self._format_response(True, data=result)
                logger.info(f"✅ [Bridge Response] {cmd_name} | Success")
                return json.dumps(response)
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"❌ [Bridge Error] {cmd_name} | {error_msg}\n{traceback.format_exc()}")
                return json.dumps(self._format_response(False, error=error_msg))

        self.registry[cmd_name] = wrapper
        self.window.bind(cmd_name, wrapper)
        logger.debug(f"Bound {cmd_name}")

    def bind_service(self, service_instance: Any, module_name: str):
        """
        Automatically binds all methods of a service instance 
        that are marked with @api_action.
        """
        logger.info(f"Binding service {service_instance.__class__.__name__} to module '{module_name}'")
        
        for attr_name in dir(service_instance):
            attr = getattr(service_instance, attr_name)
            if callable(attr) and getattr(attr, '_is_api_action', False):
                # We use the method name as the action name
                # e.g. DocumentService.get_all -> docs:get_all
                self.bind(module_name, attr_name, attr)
                
    def _format_response(self, success: bool, data: Any = None, error: str = None):
        # Automatically convert objects to dictionaries for JSON serialization
        if data is not None:
            if hasattr(data, '__dict__'):
                data = data.__dict__
            elif isinstance(data, list):
                data = [item.__dict__ if hasattr(item, '__dict__') else item for item in data]
                
        return {
            "success": success,
            "data": data,
            "error": error
        }

# Global bridge instance (initialized during app startup)
_bridge_instance = None

def get_bridge():
    global _bridge_instance
    if _bridge_instance is None:
        raise RuntimeError("Bridge not initialized. Call init_bridge(window) first.")
    return _bridge_instance

def init_bridge(window):
    global _bridge_instance
    _bridge_instance = Bridge(window)
    return _bridge_instance
