import logging
import sys
import os
import traceback
import signal
from pathlib import Path
from webui.webui import Window, set_default_root_folder, wait, get_last_error_message, Browser, exit as webui_exit
from typing import Optional

from .config import get_config
from .container import get_container

# Import API Module setup functions
from ..api.modules.docs import setup_docs_api
from ..api.modules.todos import setup_todos_api
from ..api.modules.search import setup_search_api
from ..api.modules.graph import setup_graph_api

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

_window: Optional[Window] = None

def setup_bindings(window: Window):
    """Register Python functions to be called from the frontend."""
    container = get_container()
    
    # Initialize separate API modules
    setup_docs_api(window, container)
    setup_todos_api(window, container)
    setup_search_api(window, container)
    setup_graph_api(window, container)
    
    logger.info("All API modules registered successfully")

def get_resource_path() -> Path:
    """Get the path to the web assets, supporting various bundlers."""
    # 1. Check for PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / "web"
    
    # 2. Check if running as a standalone binary (Nuitka/etc)
    # If the executable is in a different place than the script
    base_dir = Path(os.path.abspath(os.path.dirname(sys.argv[0])))
    if (base_dir / "web").exists():
        return base_dir / "web"

    # 3. Default to development path relative to this file
    dev_path = Path(__file__).parent.parent / "web"
    if dev_path.exists():
        return dev_path
    
    # 4. Fallback to project root frontend/dist
    return Path(__file__).parent.parent.parent.parent / "frontend" / "dist"

def create_window(
    title: Optional[str] = None, 
    width: Optional[int] = None, 
    height: Optional[int] = None,
    browser: Browser = Browser.Chromium
) -> Window:
    """Create and configure the main application window."""
    global _window
    
    config = get_config()
    dist_path = get_resource_path()
    
    if not config.debug and not dist_path.exists():
        logger.warning(f"Frontend folder not found at {dist_path}. Attempting to use fallback...")
        dev_dist_path = Path(__file__).parent.parent.parent.parent / "frontend" / "dist"
        if dev_dist_path.exists():
            dist_path = dev_dist_path
        else:
            logger.error(f"Frontend folder not found: {dist_path}")
            raise FileNotFoundError(f"Frontend folder not found: {dist_path}")
    
    if not config.debug:
        logger.info(f"Setting root folder to: {dist_path}")
        set_default_root_folder(str(dist_path))
    
    logger.info(f"Using browser: {browser.name}")
    
    try:
        _window = Window()
        setup_bindings(_window)
        
        if config.debug:
            url = f"http://{config.host}:{config.port}"
            logger.info(f"Debug mode enabled. Showing URL: {url}")
            if width and height:
                _window.set_size(width, height)
            else:
                _window.set_size(config.window_width, config.window_height)
            
            # Try specific browser first, then default
            if not _window.show_browser(url, browser):
                _window.show(url)
        else:
            _window.set_root_folder(str(dist_path))
            if width and height:
                _window.set_size(width, height)
            else:
                _window.set_size(config.window_width, config.window_height)
            
            logger.info("Launching GUI window...")
            # Use show() directly as it's more reliable for local files
            # and prevents the double-window bug
            _window.show("index.html")
        
        logger.info("Window created successfully")
        return _window
        
    except Exception as e:
        logger.error(f"Failed to create window: {e}")
        logger.error(traceback.format_exc())
        error_msg = get_last_error_message()
        if error_msg:
            logger.error(f"WebUI error: {error_msg}")
        raise

def get_window() -> Optional[Window]:
    return _window

def handle_signal(signum, frame):
    """Handle termination signals like Ctrl+C."""
    logger.info(f"Signal {signum} received. Closing WebUI...")
    try:
        webui_exit()
    except Exception:
        pass
    # Give it a moment to cleanup
    sys.exit(0)

def run():
    """Run the application."""
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    logger.info("Starting application...")
    try:
        create_window()
        logger.info("Entering wait loop (Press Ctrl+C to stop)...")
        wait()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        logger.error(traceback.format_exc())
        raise

def close():
    """Close the application."""
    global _window
    if _window:
        try:
            _window.destroy()
            logger.info("Window destroyed")
        except Exception as e:
            logger.error(f"Error destroying window: {e}")
        _window = None

__all__ = ['create_window', 'get_window', 'run', 'close', 'Browser']
