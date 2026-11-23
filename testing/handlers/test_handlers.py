import json
from app.core.handlers import database_error_handler
from app.core import exceptions
from app.database_models.product_model import Products
import pytest
from app.services.product_service import create_new_product

def test_database_error_handler():

    response = database_error_handler(
        request=None,
        exc=exceptions.DatabaseError("Database failed")
    )

    assert response.status_code == 500

    assert json.loads(response.body) == {
        "detail": "Internal Server error!"
    }

def test_create_product_when_seller_unauthorized(session):
    seller_login = {
        "id":1,
        "email":"hamdankhalid663@gmail.com",
        "password":("Bismillah2830")
    }

    new_product = Products(
        name="Hand free",
        price=500,
        weight="0.10gm",
        colour="white",
        brand="Ronin",
        description="This hand free sound is very smooth and soft.",
        quantity=1
    )

    with pytest.raises(exceptions.UnauthorizedSeller):
        create_new_product(new_product, session, seller_login)