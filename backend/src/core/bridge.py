import logging
import json
import traceback
from functools import wraps
from typing import Any, Callable, Dict, Optional

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
        # handlers stores the original function implementations
        self.handlers: Dict[str, Callable] = {}
        # registry stores the wrappers for direct WebUI calls
        self.registry: Dict[str, Callable] = {}
        # Initialize the unified dispatch point
        self._setup_dispatch()

    def _setup_dispatch(self):
        """Binds a single entry point for all API calls (JSON-RPC style)."""
        self.window.bind("bridge:dispatch", self.handle_dispatch)
        logger.debug("Bound unified dispatch point 'bridge:dispatch'")

    def handle_dispatch(self, event):
        """
        Unified entry point for JSON-RPC style communication.
        Expects a JSON string: { "module": "...", "action": "...", "params": { ... } }
        """
        try:
            # Extract payload from WebUI event
            arg = event.get_string() if hasattr(event, 'get_string') else event
            payload = json.loads(arg)
            
            module = payload.get('module')
            action = payload.get('action')
            params = payload.get('params')
            
            if not module or not action:
                return json.dumps(self._format_response(False, error="Missing module or action"))
            
            cmd_name = f"{module}:{action}"
            return self._execute_action(cmd_name, params)
            
        except Exception as e:
            logger.error(f"❌ [Dispatch Error] {str(e)}")
            return json.dumps(self._format_response(False, error=f"Dispatch error: {str(e)}"))

    def bind(self, module: str, action: str, handler: Callable):
        """Registers a function under a module:action namespace."""
        cmd_name = f"{module}:{action}"
        self.handlers[cmd_name] = handler
        
        # Also bind as a direct WebUI command for 'Direct' mode
        @wraps(handler)
        def wrapper(event):
            arg = event.get_string() if hasattr(event, 'get_string') else event
            return self._execute_action(cmd_name, arg)

        self.registry[cmd_name] = wrapper
        self.window.bind(cmd_name, wrapper)
        logger.debug(f"Bound {cmd_name}")

    def _execute_action(self, cmd_name: str, arg: Any) -> str:
        """Core execution logic for any bridge command."""
        handler = self.handlers.get(cmd_name)
        if not handler:
            return json.dumps(self._format_response(False, error=f"Action {cmd_name} not found"))

        logger.info(f"🚀 [Bridge Request] {cmd_name} | Arg: {arg}")
        
        try:
            # Try to parse arg as JSON if it's a string
            parsed_args = arg
            if isinstance(arg, str):
                try:
                    parsed_args = json.loads(arg)
                except json.JSONDecodeError:
                    pass

            # Execute the handler
            if isinstance(parsed_args, dict):
                result = handler(**parsed_args)
            else:
                result = handler(parsed_args)
            
            response = self._format_response(True, data=result)
            logger.info(f"✅ [Bridge Response] {cmd_name} | Success")
            return json.dumps(response)
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ [Bridge Error] {cmd_name} | {error_msg}\n{traceback.format_exc()}")
            return json.dumps(self._format_response(False, error=error_msg))

    def bind_service(self, service_instance: Any, module_name: str):
        """Automatically binds all methods of a service instance marked with @api_action."""
        logger.info(f"Binding service {service_instance.__class__.__name__} to module '{module_name}'")
        
        for attr_name in dir(service_instance):
            attr = getattr(service_instance, attr_name)
            if callable(attr) and getattr(attr, '_is_api_action', False):
                self.bind(module_name, attr_name, attr)
                
    def _format_response(self, success: bool, data: Any = None, error: str = None):
        def serialize(obj):
            if obj is None: return None
            if isinstance(obj, (int, float, str, bool)): return obj
            if hasattr(obj, 'isoformat'): return obj.isoformat()
            if hasattr(obj, 'hex'): return obj.hex
            if isinstance(obj, list): return [serialize(item) for item in obj]
            if isinstance(obj, dict): return {k: serialize(v) for k, v in obj.items()}
            if hasattr(obj, '__dict__'): return serialize(obj.__dict__)
            return str(obj)

        return {
            "success": success,
            "data": serialize(data),
            "error": error
        }

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
