import logging
import sys
import os
import traceback
import signal
import threading
from pathlib import Path
from webui.webui import Window, set_default_root_folder, wait, get_last_error_message, Browser, exit as webui_exit
from typing import Optional

from .config import get_config
from .container import get_container
from .tasks import TaskManager
from .bridge import Bridge, init_bridge, get_bridge
from shared.api import APIModules

# The separate API module setup functions are now deprecated in favor of bind_service
# but we keep them if they have complex custom logic.

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

_window: Optional[Window] = None

def setup_bindings(window: Window):
    """Register Python functions to be called from the frontend."""
    container = get_container()
    
    # 1. Initialize the Bridge
    bridge = init_bridge(window)
    
    # 2. Initialize Task Manager for concurrency
    task_manager = TaskManager()
    task_manager.set_ws_callback(lambda tid, res: logger.info(f"WebSocket Push -> Task {tid}: {res}"))
    container.register(TaskManager, task_manager, alias="task_manager")
    
    # 3. Register the bridge itself in container for service access
    container.register(Bridge, bridge, alias="bridge")
    
    # 4. Bind Services symmetrically using the APIManifest
    # Each service is bound to a module name. Methods marked with @api_action are exposed.
    services_to_bind = [
        ("docs_service", APIModules.DOCS),
        ("todo_service", APIModules.TODOS),
        ("search_service", APIModules.SEARCH),
        ("graph_service", APIModules.GRAPH),
        ("rust_service", APIModules.RUST),
        ("system_service", "system"),
        ("sys_int_service", APIModules.SYSTEM),
        ("settings_service", APIModules.SETTINGS),
        ("db_service", "db"),
    ]
    
    for service_alias, module_name in services_to_bind:
        try:
            service = container.resolve(service_alias)
            bridge.bind_service(service, module_name)
        except Exception as e:
            logger.error(f"Failed to bind service {service_alias} to {module_name}: {e}")
    
    logger.info("All services registered symmetrically via Bridge")

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
    
    if _window is not None:
        logger.info("Window already exists, returning existing instance")
        return _window
    
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
        
        # Maximize window by default to cover the entire screen size
        try:
            _window.maximize()
            logger.info("Window maximized by default")
        except Exception as e:
            logger.warning(f"Could not maximize window: {e}")
        
        if config.debug:
            url = f"http://{config.host}:{config.port}"
            logger.info(f"Debug mode enabled. Showing URL: {url}")
            if width and height:
                _window.set_size(width, height)
            else:
                _window.set_size(config.window_width, config.window_height)
            
            # Simplified window launching to avoid potential double-window issues
            logger.info(f"Debug mode enabled. Showing URL: {url}")
            _window.show(url)
        else:
            _window.set_root_folder(str(dist_path))
            if width and height:
                _window.set_size(width, height)
            else:
                _window.set_size(config.window_width, config.window_height)
            
            # Simplified window launching to avoid potential double-window issues
            logger.info("Launching GUI window...")
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
        window = create_window()
        
        # Start System Tray in a background thread
        container = get_container()
        try:
            sys_int = container.resolve("sys_int_service")
            tray_thread = threading.Thread(target=sys_int.setup_tray, args=(window,), daemon=True)
            tray_thread.start()
            logger.info("System tray started in background thread")
        except Exception as e:
            logger.warning(f"Could not start system tray: {e}")

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
