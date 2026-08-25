import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.core.config import test_database_url
from app.database_config.database_connection import get_session
from app import database_models

test_engine = create_engine(test_database_url)

# 1. Direct Dependency Override for FastAPI Client
def override_get_session():
    with Session(test_engine) as session:
        yield session

# FastAPI Dependency Override Setup
app.dependency_overrides[get_session] = override_get_session

# 2. Database Setup Fixture
@pytest.fixture(autouse=True)
def setup_database():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

# 3. Client Fixture
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

# 4. Pytest Fixture for Repository / Direct DB Tests
@pytest.fixture
def db_session():
    with Session(test_engine) as session:
        yield session