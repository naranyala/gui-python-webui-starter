import pytest
import json
from unittest.mock import MagicMock
from backend.src.core.bridge import Bridge

def test_bridge_binding_success():
    # Mock window object
    mock_window = MagicMock()
    bridge = Bridge(mock_window)
    
    # Define a simple handler
    def mock_handler(arg):
        return f"Hello {arg}"
    
    bridge.bind("test", "greet", mock_handler)
    
    # Simulate the WebUI calling the bound function
    # WebUI passes an event object; our bridge handles it
    event = MagicMock()
    event.get_string.return_value = "World"
    
    result_json = bridge.registry["test:greet"](event)
    result = json.loads(result_json)
    
    assert result["success"] is True
    assert result["data"] == "Hello World"

def test_bridge_error_handling():
    mock_window = MagicMock()
    bridge = Bridge(mock_window)
    
    def failing_handler(arg):
        raise ValueError("Something went wrong")
    
    bridge.bind("test", "fail", failing_handler)
    
    result_json = bridge.registry["test:fail"](None)
    result = json.loads(result_json)
    
    assert result["success"] is False
    assert "Something went wrong" in result["error"]

def test_bridge_argument_passing():
    mock_window = MagicMock()
    bridge = Bridge(mock_window)
    
    def identity_handler(arg):
        return arg
    
    bridge.bind("test", "echo", identity_handler)
    
    # Test with raw string (simulating fallback)
    result_json = bridge.registry["test:echo"]("RawString")
    result = json.loads(result_json)
    assert result["data"] == "RawString"
