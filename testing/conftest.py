from app.database_models.admin_model import Admin
from app.database_models.user_model import Users
from app.database_models.cart_model import Cart
from app.database_models.order_model import Orders
from app.database_models.product_model import Products
from app.database_models.seller_model import Sellers
from app.core.jwt_token import create_token
from fastapi.testclient import TestClient
from app.main import app
from app.database_config.database_connection import get_session


import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

# Separate testing database
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Create tables before testing
@pytest.fixture()
def session():
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture()
def client(session):

    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def seller():
    seller_data = {
        "id": 1,
        "email": "hamdan@gmail.com"
    }

    token = create_token(seller_data)
    return token