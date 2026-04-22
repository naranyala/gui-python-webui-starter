import pytest
import threading
import time
from backend.src.core.container import DIContainer
from backend.src.services import DocumentService
from backend.src.core.database import Database, get_db

def test_sqlite_wal_concurrency(tmp_path):
    """
    Stress test SQLite WAL mode by performing simultaneous 
    writes and reads using separate connections per thread.
    """
    db_path = str(tmp_path / "concurrency_test.db")
    
    # Initial setup to create the DB and tables
    db = Database(db_path)
    db.connect()
    
    # We create a helper to get a fresh service with its own connection
    def create_service():
        # Override get_db for this specific instance to avoid singleton issues in threads
        import backend.src.core.database as db_mod
        original_get_db = db_mod.get_db
        db_mod.get_db = lambda path=db_path: Database(db_path)
        
        container = DIContainer()
        service = DocumentService(container)
        service.on_initialize()
        return service, original_get_db

    results = []
    errors = []
    
    def writer():
        try:
            service, original_get_db = create_service()
            for i in range(50):
                service.create(f"Title {i}", f"Content {i}")
                time.sleep(0.001)
        except Exception as e:
            errors.append(e)
    
    def reader():
        try:
            service, original_get_db = create_service()
            for _ in range(50):
                docs = service.get_all()
                results.append(len(docs))
                time.sleep(0.001)
        except Exception as e:
            errors.append(e)

    # Launch multiple writers and readers
    threads = []
    for _ in range(3):
        threads.append(threading.Thread(target=writer))
    for _ in range(3):
        threads.append(threading.Thread(target=reader))
        
    for t in threads: t.start()
    for t in threads: t.join()
    
    # Verification
    assert len(errors) == 0, f"Encountered concurrency errors: {errors}"
    
    # Final check with a clean connection
    container = DIContainer()
    service = DocumentService(container)
    service.on_initialize()
    # 3 writers * 50 docs = 150 docs total. 
    # Note: we might have more if on_initialize seeds docs.
    # The a-priori count depends on how many docs are in the seed list.
    # Let's just check that we have at least the 150 we wrote.
    assert len(service.get_all()) >= 150
