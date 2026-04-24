from typing import Type, TypeVar, Dict, Any, Optional

T = TypeVar('T')

class DIContainer:
    """
    A lightweight Dependency Injection container.
    Stores service instances as singletons keyed by their class type or a string alias.
    """
    def __init__(self):
        self._services: Dict[Any, Any] = {}

    def register(self, service_cls: Type[T], instance: T, alias: Optional[str] = None) -> None:
        """Register a pre-instantiated service instance."""
        self._services[service_cls] = instance
        if alias:
            self._services[alias] = instance

    def resolve(self, identifier: Any) -> Any:
        """Resolve a service instance by its class type or string alias."""
        if identifier not in self._services:
            name = identifier.__name__ if hasattr(identifier, '__name__') else str(identifier)
            raise KeyError(f"Service {name} not registered in DIContainer")
        return self._services[identifier]

    def __contains__(self, item: object) -> bool:
        return item in self._services

    def __contains__(self, item: object) -> bool:
        return item in self._services

# Global container instance
_container = DIContainer()

def get_container() -> DIContainer:
    return _container

def set_container(container: DIContainer) -> None:
    global _container
    _container = container

__all__ = ['DIContainer', 'get_container', 'set_container']
