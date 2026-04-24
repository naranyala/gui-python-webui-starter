import subprocess
import json
import logging
import os
from typing import Dict, Any, Optional
from ..core.bridge import api_action

logger = logging.getLogger(__name__)

class RustCliService:
    """
    Service that interfaces with Rust-written CLI tools.
    """
    def __init__(self, container):
        self.container = container
        # In production, this would be a config setting
        self.bin_path = os.path.abspath("cli-rs/file-analyzer/target/release/file-analyzer")

    def initialize(self):
        if not os.path.exists(self.bin_path):
            logger.error(f"Rust binary not found at {self.bin_path}. Please run 'cargo build --release' in cli-rs/file-analyzer")
            return False
        logger.info(f"Rust CLI Service initialized. Binary: {self.bin_path}")
        return True

    @api_action
    def analyze_directory(self, path: str) -> Dict[str, Any]:
        """
        Calls the Rust file-analyzer CLI to get directory statistics.
        """
        try:
            logger.info(f"Running Rust analyzer on path: {path}")
            
            # Call the binary
            result = subprocess.run(
                [self.bin_path, path],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse JSON output
            return json.loads(result.stdout)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Rust CLI execution failed: {e.stderr}")
            return {
                "total_files": 0,
                "total_size": 0,
                "largest_files": [],
                "error": f"CLI Error: {e.stderr or str(e)}"
            }
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Rust CLI output: {e}")
            return {
                "total_files": 0,
                "total_size": 0,
                "largest_files": [],
                "error": "Failed to parse response from Rust tool"
            }
        except Exception as e:
            logger.error(f"Unexpected error running Rust CLI: {e}")
            return {
                "total_files": 0,
                "total_size": 0,
                "largest_files": [],
                "error": str(e)
            }
