import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import TEST_DATABASE_URL
from src.database import get_db
from src.main import app
from src.models import Base

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(setup_test_db):
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client


# Fixture to generate a task payload
@pytest.fixture()
def task_payload():
    """Generate a task payload."""
    return {
        "title": "New test task",
        "description": "This is a test task",
        "completed": False,
    }


@pytest.fixture()
def task_payload_updated():
    """Generate an updated task payload."""
    return {
        "title": "Modified task",
        "description": "This is a modified task",
        "completed": True,
    }