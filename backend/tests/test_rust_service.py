import pytest
import json
from unittest.mock import patch, MagicMock
from backend.src.services.RustCliService import RustCliService

def test_rust_service_parsing():
    # Mock container
    mock_container = MagicMock()
    service = RustCliService(mock_container)
    
    # Mock the Rust binary output
    mock_output = json.dumps({
        "total_files": 10,
        "total_size": 1024,
        "largest_files": [{"path": "test.txt", "size": 100}],
        "error": None
    })
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout=mock_output, returncode=0)
        
        result = service.analyze_directory("/tmp")
        
        assert result["total_files"] == 10
        assert result["total_size"] == 1024
        assert result["largest_files"][0]["path"] == "test.txt"

def test_rust_service_error():
    mock_container = MagicMock()
    service = RustCliService(mock_container)
    
    with patch('subprocess.run') as mock_run:
        # Simulate a crash
        mock_run.side_effect = Exception("Binary not found")
        
        result = service.analyze_directory("/tmp")
        assert "error" in result
        assert "Binary not found" in result["error"]
