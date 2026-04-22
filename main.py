import sys
import os
import logging
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.src.core import set_container, DIContainer
from backend.src.core.config import AppConfig, set_config
from backend.src.core.app import run, close
from backend.src.services import DocumentService, SearchService, GraphService, TodoService, SystemService, SettingsService
from backend.src.api.server import start_api_server

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def configure_services(container: DIContainer):
    """Register all services in the container."""
    logger.info("Registering services...")
    
    # Instantiate services (Dependency Injection happens here)
    # In a more complex app, you'd pass dependencies into the constructors
    doc_service = DocumentService(container)
    search_service = SearchService(container)
    graph_service = GraphService(container)
    todo_service = TodoService(container)
    system_service = SystemService(container)
    settings_service = SettingsService(container)
    
    # Register as singletons
    container.register(DocumentService, doc_service)
    container.register(SearchService, search_service)
    container.register(GraphService, graph_service)
    container.register(TodoService, todo_service)
    container.register(SystemService, system_service)
    container.register(SettingsService, settings_service)
    
    logger.info("Initializing services...")
    for service in [doc_service, search_service, graph_service, todo_service, system_service, settings_service]:
        try:
            service.initialize()
            logger.info(f"Initialized {service.__class__.__name__}")
        except Exception as e:
            logger.error(f"Failed to initialize {service.__class__.__name__}: {e}")
            raise

def main():
    """Main entry point."""
    logger.info("=" * 50)
    logger.info("Starting DocViewer Application")
    logger.info("=" * 50)
    
    try:
        config = AppConfig.from_env()
        set_config(config)
        logger.info(f"Loaded config: {config.app_name} v{config.app_version}")
        
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        traceback.print_exc()
        return 1
    
    try:
        container = DIContainer()
        set_container(container)
        configure_services(container)
        
    except Exception as e:
        logger.error(f"Failed to configure services: {e}")
        traceback.print_exc()
        return 1
    
    try:
        # Start background API server (FastAPI)
        logger.info("Starting API server...")
        start_api_server(port=8000)
        
        run()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Application stopped")
    except Exception as e:
        logger.error(f"Application runtime error: {e}")
        traceback.print_exc()
        return 1
    finally:
        try:
            close()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    logger.info("Application exited normally")
    return 0

if __name__ == "__main__":
    sys.exit(main())