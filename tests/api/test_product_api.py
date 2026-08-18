from unittest.mock import patch
from app.api.product_api import get_user_token
from app.main import app
from app.core import exceptions
from sqlalchemy.exc import DatabaseError
from app.database_models.product_model import UpdateProduct

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

def test_database_error_for_creating_product(client):
    product = {
        "name": "Chocolate",
        "price": 2000,
        "weight": "1kg",
        "colour": "Black",
        "brand": "Nutella",
        "description": "Nutella chocolate is very good for health.",
        "quantity": 50
    }

    with patch(
        "app.api.product_api.create_new_product", 
        side_effect=DatabaseError(
            statement="Create Product",
            params={},
            orig=Exception("Database connection failed")
    )
    ) as fake_product_result:

        seller = client.post(
            "/products",
            json = product
        )

        assert seller.status_code == 500
        fake_product_result.assert_called_once()

def test_product_update_api_successfully(client):
    product_update = UpdateProduct(
        quantity=40
    )
    with patch(
        "app.api.product_api.update_seller_product_attributes", return_value={"Message" : "Product successfully updated"}
    ):
        seller = client.patch(
            "/product/3",
            json=product_update.model_dump()
        )

        assert seller.status_code == 200
        assert seller.json() == {"Message" : "Product successfully updated"}

def test_product_update_but_seller_not_found(client):
    product_update = UpdateProduct(
        quantity=40
    )
    with patch(
        "app.api.product_api.update_seller_product_attributes", 
            side_effect=exceptions.UnauthorizedSeller
    ):
        seller = client.patch(
            "/product/3",
            json=product_update.model_dump()
        )

        assert seller.status_code == 401
        assert seller.json() == {
            "detail" : "Unauthorized Seller!"
        }

def test_product_update_but_product_not_found(client):
    product_update = UpdateProduct(
        quantity=40
    )
    with patch(
        "app.api.product_api.update_seller_product_attributes", 
            side_effect=exceptions.ProductNotFound
    ):
        seller = client.patch(
            "/product/3",
            json=product_update.model_dump()
        )

        assert seller.status_code == 404
        assert seller.json() == {
            "detail" : "Product not found"
        }

def test_product_update_but_seller_product_not_found(client):
    product_update = UpdateProduct(
        quantity=40
    )
    with patch(
        "app.api.product_api.update_seller_product_attributes", 
            side_effect=exceptions.SellerProductNotFound
    ):
        seller = client.patch(
            "/product/3",
            json=product_update.model_dump()
        )

        assert seller.status_code == 403
        assert seller.json() == {
            "detail" : "Product not found!"
        }


def test_product_update_but_database_error(client):
    product_update = UpdateProduct(
        quantity=40
    )
    with patch(
        "app.api.product_api.update_seller_product_attributes", 
            side_effect=DatabaseError(
            statement="UPDATE products SET quantity = 40 WHERE id = 3",
            params={},
            orig=Exception("Database connection failed")
    )
    ):
        seller = client.patch(
            "/product/3",
            json=product_update.model_dump()
        )

        assert seller.status_code == 500
        assert seller.json() == {
            "detail" : "Internal Server error!"
        }
