import pytest
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
        
        test_db = Database(db_path)
        database._db = test_db # Inject test db
        
        service = DocumentService(container)
        service.initialize()
        yield service
        
        test_db.close()
        database._db = None # Reset

    def test_create_and_get_all(self, service):
        # Initial data (seeded docs)
        initial_count = len(service.get_all())
        
        # Create new
        new_doc = service.create("Test Title", "Test Content")
        assert new_doc.title == "Test Title"
        
        # Verify count increased
        docs = service.get_all()
        assert len(docs) == initial_count + 1
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

    def test_document_boundaries(self, service):
        """Test documents with extreme sizes and empty content."""
        # 1. Empty title and content
        doc_empty = service.create("", "")
        assert doc_empty.title == ""
        assert doc_empty.content == ""
        
        # 2. Very large content (1MB)
        large_content = "A" * (1024 * 1024)
        doc_large = service.create("Large Doc", large_content)
        retrieved = service.get_by_id(doc_large.id)
        assert retrieved.content == large_content
