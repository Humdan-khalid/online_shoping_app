from app.api.product_api import new_product
from unittest.mock import patch, Mock
from app.api.product_api import get_user_token
from app.main import app
import pytest
from app.core import exceptions
from sqlalchemy.exc import DatabaseError

def test_create_new_product_successfully(client):


    return_seller_product = {
        "name": "Ballon",
        "price": 20,
        "weight": "0.5kg",
        "colour": "White",
        "brand": "Shenin",
        "description": "This ballon quality is very good.",
        "quantity": 30
    }

    app.dependency_overrides[get_user_token] = lambda: {
        "id": 1,
        "email": "hamdan@gmail.com"
    }

    with patch("app.api.product_api.create_new_product", return_value=return_seller_product) as fake_created_product:
        seller = client.post(
            "/products",
            json={
                "name": "Ballon",
                "price": 20,
                "weight": "0.5kg",
                "colour": "White",
                "brand": "Shenin",
                "description": "This ballon quality is very good.",
                "quantity": 30
                }
            
            
        )

        assert seller.status_code == 201
        fake_created_product.assert_called_once()



def test_token_not_found_for_product_create(client):

    return_seller_product = {
        "name": "Ballon",
        "price": 20,
        "weight": "0.5kg",
        "colour": "White",
        "brand": "Shenin",
        "description": "This ballon quality is very good.",
        "quantity": 30
    }

    with patch("app.api.product_api.create_new_product", 
               side_effect = exceptions.InvalidToken) as fake_created_product:


        seller = client.post(
            "/products",
            json=return_seller_product
        )

        assert seller.status_code == 401
        assert seller.json() == {
            "detail": "Unauthorized Seller!"
        }

        fake_created_product.assert_called_once()

# def test_database_error_for_creating_product(client):
#     product = {
#         "name": "Chocolate",
#         "price": 2000,
#         "weight": "1kg",
#         "colour": "Black",
#         "brand": "Nutella",
#         "description": "Nutella chocolate is very good for health.",
#         "quantity": 50
#     }

#     with patch(
#         "app.api.product_api.create_new_product", side_effect=DatabaseError("Internal Server Error!")
#     ) as fake_product_result:

#         seller = client.post(
#             "/products",
#             json = product
#         )

#         assert seller.status_code == 500