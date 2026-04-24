import pytest
import time
from backend.src.core.tasks import TaskManager

def test_task_manager_execution():
    manager = TaskManager()
    results = []
    
    def callback(tid, res):
        results.append(res)
        
    manager.set_ws_callback(callback)
    
    def slow_task(x):
        time.sleep(0.1)
        return x * 2
    
    task_id = manager.submit(slow_task, 21)
    
    assert task_id is not None
    assert manager.get_status(task_id) == "running"
    
    # Wait for completion
    time.sleep(0.2)
    
    assert manager.get_status(task_id) == "completed"
    assert len(results) == 1
    assert results[0]["data"] == 42

def test_task_manager_error():
    manager = TaskManager()
    results = []
    manager.set_ws_callback(lambda tid, res: results.append(res))
    
    def failing_task():
        raise RuntimeError("Task failed!")
        
    task_id = manager.submit(failing_task)
    time.sleep(0.1)
    
    assert results[0]["success"] is False
    assert "Task failed!" in results[0]["error"]
