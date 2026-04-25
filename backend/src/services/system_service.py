from typing import Dict, Any
from .base import BaseService
from ..core.bridge import api_action
import psutil
import platform

class SystemService(BaseService):
    """Service for monitoring system resources."""
    
    @api_action
    def get_stats(self) -> Dict[str, Any]:
        """Returns current system resource usage."""
        return {
            "cpu": psutil.cpu_percent(interval=None),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage('/')._asdict(),
            "os": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
            }
        }
