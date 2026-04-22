import pytest
import os
import sqlite3
from backend.src.services.document_service import DocumentService
from backend.src.core.database import Database
from backend.src.core.container import DIContainer

class TestDocumentService:
    @pytest.fixture
    def db_path(self, tmp_path):
        return str(tmp_path / "test_app.db")

    @pytest.fixture
    def container(self):
        return DIContainer()

    @pytest.fixture
    def service(self, container, db_path):
        # We need to monkeypatch the database path for testing
        from backend.src.core import database
        original_get_db = database.get_db
        
        test_db = Database(db_path)
        database._db = test_db # Inject test db
        
        service = DocumentService(container)
        service.initialize()
        yield service
        
        test_db.close()
        database._db = None # Reset

    def test_create_and_get_all(self, service):
        # Initial data (1 doc from init_db)
        docs = service.get_all()
        assert len(docs) == 1
        
        # Create new
        new_doc = service.create("Test Title", "Test Content")
        assert new_doc.title == "Test Title"
        
        # Verify count
        docs = service.get_all()
        assert len(docs) == 2
        assert any(d.id == new_doc.id for d in docs)

    def test_get_by_id(self, service):
        new_doc = service.create("Search Me", "Content")
        found = service.get_by_id(new_doc.id)
        assert found is not None
        assert found.title == "Search Me"
        
        assert service.get_by_id("non-existent") is None

    def test_update(self, service):
        doc = service.create("Old Title", "Old Content")
        updated = service.update(doc.id, title="New Title")
        
        assert updated.title == "New Title"
        assert updated.content == "Old Content" # Unchanged
        
        # Verify persistence
        reloaded = service.get_by_id(doc.id)
        assert reloaded.title == "New Title"

    def test_delete(self, service):
        doc = service.create("To Delete", "...")
        assert service.delete(doc.id) is True
        assert service.get_by_id(doc.id) is None
        assert service.delete(doc.id) is False
