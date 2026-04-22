from typing import Type, Callable, Any, TypeVar, get_type_hints
from dataclasses import dataclass
from functools import lru_cache

T = TypeVar('T')

@dataclass
class ServiceDescriptor:
    factory: Callable
    singleton: bool
    instance: Any = None

class DIContainer:
    def __init__(self):
        self._services: dict[Type, ServiceDescriptor] = {}
    
    def register(
        self, 
        token: Type[T], 
        factory: Callable[['DIContainer'], T] = None,
        singleton: bool = True
    ) -> 'DIContainer':
        if factory is None:
            # Use token as factory if it's callable
            def default_factory(container):
                return token(container)
            factory = default_factory
        
        self._services[token] = ServiceDescriptor(
            factory=factory,
            singleton=singleton
        )
        return self
    
    def register_instance(self, token: Type[T], instance: T) -> 'DIContainer':
        self._services[token] = ServiceDescriptor(
            factory=lambda _: instance,
            singleton=True,
            instance=instance
        )
        return self
    
    def register_factory(
        self,
        token: Type[T],
        factory: Callable[['DIContainer'], T]
    ) -> 'DIContainer':
        return self.register(token, factory, singleton=False)
    
    def resolve(self, token: Type[T]) -> T:
        if token not in self._services:
            raise KeyError(f"Service {token} not registered")
        
        descriptor = self._services[token]
        
        if descriptor.singleton:
            if descriptor.instance is None:
                descriptor.instance = descriptor.factory(self)
            return descriptor.instance
        return descriptor.factory(self)
    
    def has(self, token: Type) -> bool:
        return token in self._services
    
    def clear(self):
        self._services.clear()

# Global container instance
_container: DIContainer = DIContainer()

def get_container() -> DIContainer:
    return _container

def set_container(container: DIContainer):
    global _container
    _container = container

__all__ = ['DIContainer', 'get_container', 'set_container', 'ServiceDescriptor']