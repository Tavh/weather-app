import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app import create_app
from app.core.database import Base, get_session

# 1. Create a SINGLE in-memory engine for the entire test session
TEST_ENGINE = create_engine("sqlite:///:memory:")

@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each test session."""
    app_instance = create_app()
    app_instance.app.config.update({
        "TESTING": True,
        # We don't actually use this config for the session fixture logic below,
        # but it's good practice.
        "DATABASE_URL": "sqlite:///:memory:"
    })
    
    # Create tables once
    Base.metadata.create_all(bind=TEST_ENGINE)
    
    yield app_instance.app
    
    # Drop tables after suite
    Base.metadata.drop_all(bind=TEST_ENGINE)

@pytest.fixture(scope="function")
def session(app):
    """
    Creates a new database session for a test.
    Rolls back transaction at the end so tests are isolated.
    This MAGICALLY overrides the 'get_session' dependency in the app if we patch it,
    OR we rely on the fact that we're mostly testing via client API which uses its own session.
    
    CRITICAL: For client integration tests to share this isolation, 
    we must ensure the API uses the SAME connection.
    """
    connection = TEST_ENGINE.connect()
    transaction = connection.begin()
    
    # Bind a new session to this specific connection
    # so logic inside the test (creating seed data) uses it
    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)
    
    # Hack: We need the API to use THIS session factory or engine.
    # Since our 'get_session' in database.py creates a new SessionLocal(),
    # determining how to inject this isolated session into the running API 
    # is tricky without a dependency override system.
    
    # SIMPLER STRATEGY for this specific codebase:
    # 1. Monkeypatch 'app.core.database.SessionLocal' to return our test-scoped session
    # 2. This ensures API calls use this transaction-bound session.
    import app.core.database
    original_session_local = app.core.database.SessionLocal
    app.core.database.SessionLocal = session_factory
    
    yield session
    
    # Restore
    app.core.database.SessionLocal = original_session_local
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(app, session):
    """A test client for the app, depending on the session fixture to ensure monkeypatching is active."""
    return app.test_client()

@pytest.fixture
def auth_header(client):
    """Helper to get an auth header for a fresh user."""
    from tests.constants import DEFAULT_USERNAME, DEFAULT_PASSWORD
    # Register & Login
    client.post("/api/v1/auth/register", json={
        "username": DEFAULT_USERNAME,
        "password": DEFAULT_PASSWORD
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": DEFAULT_USERNAME, 
        "password": DEFAULT_PASSWORD
    })
    token = resp.json["access_token"]
    return {"Authorization": f"Bearer {token}"}
