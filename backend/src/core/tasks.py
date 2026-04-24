import logging
import uuid
import concurrent.futures
from typing import Callable, Any, Dict
from .config import get_config

logger = logging.getLogger(__name__)

class TaskManager:
    """
    Handles background execution of heavy tasks to prevent GUI freezing.
    """
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.tasks: Dict[str, Any] = {}
        self._ws_callback = None

    def set_ws_callback(self, callback: Callable[[str, Any], None]):
        """Set the function used to push results to the frontend via WebSocket."""
        self._ws_callback = callback

    def submit(self, func: Callable, *args, **kwargs) -> str:
        task_id = str(uuid.uuid4())
        logger.info(f"Submitting background task {task_id}: {func.__name__}")
        
        # Wrap the function to handle completion
        def wrapped():
            try:
                result = func(*args, **kwargs)
                self._complete_task(task_id, {"success": True, "data": result})
            except Exception as e:
                logger.error(f"Task {task_id} failed: {e}")
                self._complete_task(task_id, {"success": False, "error": str(e)})

        self.tasks[task_id] = "running"
        self.executor.submit(wrapped)
        return task_id

    def _complete_task(self, task_id: str, result: Any):
        self.tasks[task_id] = "completed"
        if self._ws_callback:
            # Push result via WebSocket: { type: 'task_result', taskId: '...', data: { ... } }
            self._ws_callback(task_id, result)
        else:
            logger.warning(f"Task {task_id} completed but no WebSocket callback configured")

    def get_status(self, task_id: str) -> str:
        return self.tasks.get(task_id, "not_found")

    def shutdown(self):
        self.executor.shutdown(wait=False)
