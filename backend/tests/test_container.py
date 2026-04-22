import pytest
from backend.src.core.container import DIContainer

class MockService:
    def __init__(self, container):
        self.container = container

def test_container_registration():
    container = DIContainer()
    service = MockService(container)
    container.register(MockService, service)
    assert container.resolve(MockService) == service

def test_container_singleton():
    container = DIContainer()
    service = MockService(container)
    container.register(MockService, service)
    assert container.resolve(MockService) is container.resolve(MockService)

def test_container_missing():
    container = DIContainer()
    with pytest.raises(KeyError):
        container.resolve(MockService)
