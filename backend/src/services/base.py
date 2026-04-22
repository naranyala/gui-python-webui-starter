from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.container import DIContainer

class IService(ABC):
    """Base interface for all services."""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the service."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Cleanup resources."""
        pass

class BaseService(IService):
    """Base class for all services with DI support."""
    
    def __init__(self, container: 'DIContainer'):
        self._container = container
        self._initialized = False
    
    @property
    def container(self) -> 'DIContainer':
        return self._container
    
    def initialize(self) -> None:
        if not self._initialized:
            self.on_initialize()
            self._initialized = True
    
    def shutdown(self) -> None:
        if self._initialized:
            self.on_shutdown()
            self._initialized = False
    
    def on_initialize(self) -> None:
        """Override in subclass for custom initialization."""
        pass
    
    def on_shutdown(self) -> None:
        """Override in subclass for custom cleanup."""
        pass
    
    def ensure_initialized(self) -> None:
        if not self._initialized:
            raise RuntimeError(f"{self.__class__.__name__} not initialized. Call initialize() first.")

__all__ = ['IService', 'BaseService']