from app.services.product_service import create_new_product, update_product_attributes
from unittest.mock import patch, Mock
import pytest
from app.core import exceptions
from app.database_models.product_model import UpdateProduct

def test_create_product_but_seller_not_found():

    product = Mock()
    session = Mock()
    token = {
        "id": 1,
        "email": "hamdan@gmail.com"
    }

    with patch("app.services.product_service.get_seller_from_token", return_value=None) as fake_seller_verify:
        with pytest.raises(exceptions.InvalidToken):
            create_new_product(product, session, token)


def test_create_product_successfully():

    fake_product = Mock()

    fake_product.name = "Soft-Drink"
    fake_product.price = 200
    fake_product.weight = "300ml"
    fake_product.colour = "Black"
    fake_product.brand = "Gucci"
    fake_product.description = "This soft drink is very healthy."
    fake_product.quantity = 20

    fake_session = Mock()

    token = {
        "id": 1,
        "email": "hamdan@gmail.com"
    }

    fake_seller = Mock()

    fake_seller.id = 1,
    fake_seller.email="hannan@gmail.com"

    with patch("app.services.product_service.get_seller_from_token", return_value=fake_seller) as fake_seller_verify:
        with patch("app.services.product_service.product_save_in_database") as fake_database:
           result = create_new_product(fake_product, fake_session, token)

        assert result.name == "Soft-Drink"
        fake_seller_verify.assert_called_once_with(token, fake_session)
        fake_database.assert_called_once()


def test_update_product_failed():
    product_update = Mock()
    product_update.quantity = "90"
    
    product_id: int = 2

    seller: dict = {
        "id": 3,
        "email": "hamdan@gmail.com"
    }

    session = Mock()


    with patch("app.services.product_service.get_seller_from_token", return_value = None):
        with pytest.raises(exceptions.UnauthorizedSeller):
            updated = update_product_attributes(product_id, product_update, seller, session)
            updated.assert_called_once()