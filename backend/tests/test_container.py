import pytest
from backend.src.core.container import DIContainer

class MockService:
    def __init__(self, container):
        self.container = container
        self.initialized = False
    def initialize(self):
        self.initialized = True

def test_container_registration():
    container = DIContainer()
    container.register(MockService)
    
    assert container.has(MockService)
    
    service = container.resolve(MockService)
    assert isinstance(service, MockService)
    assert service.container == container

def test_container_singleton():
    container = DIContainer()
    container.register(MockService)
    
    s1 = container.resolve(MockService)
    s2 = container.resolve(MockService)
    
    assert s1 is s2

def test_container_factory():
    container = DIContainer()
    container.register_factory(MockService, lambda c: MockService(c))
    
    s1 = container.resolve(MockService)
    s2 = container.resolve(MockService)
    
    assert s1 is not s2
