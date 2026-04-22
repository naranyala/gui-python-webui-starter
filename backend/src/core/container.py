from typing import Type, TypeVar, Dict, Any, Optional

T = TypeVar('T')

class DIContainer:
    """
    A lightweight Dependency Injection container.
    Stores service instances as singletons keyed by their class type.
    """
    def __init__(self):
        self._services: Dict[Type, Any] = {}

    def register(self, service_cls: Type[T], instance: T) -> None:
        """Register a pre-instantiated service instance."""
        self._services[service_cls] = instance

    def resolve(self, service_cls: Type[T]) -> T:
        """Resolve a service instance by its class type."""
        if service_cls not in self._services:
            raise KeyError(f"Service {service_cls.__name__} not registered in DIContainer")
        return self._services[service_cls]

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
