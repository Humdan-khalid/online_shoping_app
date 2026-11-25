from app.services.product_service import create_new_product, update_product_attributes
import pytest
from app.core import exceptions
from app.database_models.seller_model import Sellers
from app.database_models.product_model import Products, UpdateProduct
from app.utils.password_hash import create_hash_password
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError

def test_create_new_product_database_error(session):
    seller = Sellers(
        name="Hamdan Khalid",
        age=20,
        phone_number="03190286038",
        city="Karachi",
        email="hamdankhalid663@gmail.com",
        password=create_hash_password("Bismillah2830")
    )

    session.add(seller)
    session.commit()
    session.refresh(seller)

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

    with patch("app.services.product_service.product_save_in_database",
               side_effect=SQLAlchemyError):
        with pytest.raises(exceptions.DatabaseError):
            create_new_product(new_product, session, seller_login)


def test_product_created_successfully(session):
    seller = Sellers(
        name="Hamdan Khalid",
        age=20,
        phone_number="03190286038",
        city="Karachi",
        email="hamdankhalid663@gmail.com",
        password=create_hash_password("Bismillah2830")
    )

    session.add(seller)
    session.commit()
    session.refresh(seller)

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

    result = create_new_product(new_product, session, seller_login)

    assert result.name == "Hand free" 
    assert result.quantity == 1

def test_product_update_unauthorized_seller_error(session):
    new_seller = Sellers(
        name="Hamdan Khalid",
        age=20,
        phone_number="03190286038",
        city="Karachi",
        email="hamdankhalid663@gmail.com",
        password=create_hash_password("Bismillah2830")
    )

    session.add(new_seller)
    session.commit()
    session.refresh(new_seller)

    seller = new_seller.model_dump()

    product = UpdateProduct(
        price=520.0,
        quantity=100
    )

    with patch(
        "app.services.product_service.get_seller_from_token",
        return_value=None
    ):
        with pytest.raises(exceptions.UnauthorizedSeller):
            update_product_attributes(1, product, seller, session)