from app.services.product_service import create_new_product, update_seller_product_attributes
from unittest.mock import patch, Mock
import pytest
from app.core import exceptions
from app.database_models.product_model import UpdateProduct, Products

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

def test_product_update_successfully():
    session = Mock()
    db_seller = Mock()

    db_seller.id = 1
    db_seller.email = "hamdankhalid@gmail.com"

    seller = {
            "id" : 1,
            "email" : "hamdankhalid@gmail.com"
    }

    product = Products()
    product.id = 2
    product.name = "Hair Shampoo"
    product.price = 600
    product.seller_id = 1
    product.status = "Available"

    update_data = UpdateProduct(price=650)

    with patch(
        "app.services.product_service.get_seller_from_token", return_value=db_seller
    ) as mock_get_seller:

        with patch(
            "app.services.product_service.find_product_in_database", return_value=product
        ) as mock_get_product_in_database:
            
            with patch(
            "app.services.product_service.find_seller_product_in_database", return_value=product
        ) as mock_get_seller_product_in_database:
               
               with patch(
                   "app.services.product_service.delete_seller_products_in_cache"
                ) as mock_delete_products_in_cache:

                result = update_seller_product_attributes(2, update_data, seller, session)

                mock_get_seller.assert_called_once_with(seller, session)
                mock_get_product_in_database.assert_called_once_with(2, session)
                mock_get_seller_product_in_database.assert_called_once_with(2, seller["id"], session)
                mock_delete_products_in_cache(db_seller.id)

                assert product.price == 650

                session.add.assert_called_once_with(product)
                session.commit.assert_called_once()


def test_update_product_but_seller_not_found():
    session = Mock()

    seller = {
            "id" : 1,
            "email" : "hamdankhalid@gmail.com"
    }

    update_data = UpdateProduct(price=650)

    with patch(
        "app.services.product_service.get_seller_from_token", return_value=None
    ) as mock_get_seller_in_database:
        with pytest.raises(
            exceptions.UnauthorizedSeller
        ):
            update_seller_product_attributes(2, update_data, seller, session)
            mock_get_seller_in_database.assert_called_once_with(seller, session)

def test_update_product_but_product_not_found():
    session = Mock()
    db_seller = Mock()

    db_seller.id = 1
    db_seller.email = "hamdankhalid@gmail.com"

    seller = {
            "id" : 1,
            "email" : "hamdankhalid@gmail.com"
    }

    update_data = UpdateProduct(price=300)

    with patch(
        "app.services.product_service.get_seller_from_token", return_value=db_seller
    ) as mock_get_seller:

        with patch(
            "app.services.product_service.find_product_in_database", return_value=None
        ) as mock_get_product_in_database:

            with pytest.raises(
                exceptions.ProductNotFound
            ):
                update_seller_product_attributes(2, update_data, seller, session)
    mock_get_seller.assert_called_once_with(seller, session)
    mock_get_product_in_database.assert_called_once_with(2, session)


def test_update_product_but_seller_product_not_found():
    session = Mock()
    db_seller = Mock()

    db_seller.id = 1
    db_seller.email = "hamdankhalid@gmail.com"

    seller = {
            "id" : 1,
            "email" : "hamdankhalid@gmail.com"
    }

    product = Products()
    product.id = 2
    product.name = "Hair Shampoo"
    product.price = 600
    product.seller_id = 5
    product.status = "Available"

    update_data = UpdateProduct(price=650)

    with patch(
        "app.services.product_service.get_seller_from_token", return_value=db_seller
    ) as mock_get_seller:

        with patch(
            "app.services.product_service.find_product_in_database", return_value=product
        ) as mock_get_product_in_database:
            
            with patch(
            "app.services.product_service.find_seller_product_in_database", return_value=None
        ) as mock_get_seller_product_in_database:

                with pytest.raises(
                    exceptions.SellerProductNotFound
                ):
                    update_seller_product_attributes(2, update_data, seller, session)
               

        mock_get_seller.assert_called_once_with(seller, session)
        mock_get_product_in_database.assert_called_once_with(2, session)
        mock_get_seller_product_in_database.assert_called_once_with(2, seller["id"], session)

        assert product.price != 650
        assert product.price == 600

def test_update_product_but_seller_product_not_available():
    session = Mock()
    db_seller = Mock()

    db_seller.id = 1
    db_seller.email = "hamdankhalid@gmail.com"

    seller = {
            "id" : 1,
            "email" : "hamdankhalid@gmail.com"
    }

    product = Products()
    product.id = 2
    product.name = "Hair Shampoo"
    product.price = 600
    product.seller_id = 5
    product.status = "Not Available"

    update_data = UpdateProduct(price=650)

    with patch(
        "app.services.product_service.get_seller_from_token", return_value=db_seller
    ) as mock_get_seller:

        with patch(
            "app.services.product_service.find_product_in_database", return_value=product
        ) as mock_get_product_in_database:
            
            with patch(
            "app.services.product_service.find_seller_product_in_database", return_value=product
        ) as mock_get_seller_product_in_database:

                with pytest.raises(
                    exceptions.SellerProductNotFound
                ):
                    update_seller_product_attributes(2, update_data, seller, session)
               

        mock_get_seller.assert_called_once_with(seller, session)
        mock_get_product_in_database.assert_called_once_with(2, session)
        mock_get_seller_product_in_database.assert_called_once_with(2, seller["id"], session)

        assert product.price != 650
        assert product.price == 600


def test_product_update_database_error():
    session = Mock()
    db_seller = Mock()

    session.add.side_effect = exceptions.DatabaseError("Database error")

    db_seller.id = 1
    db_seller.email = "hamdankhalid@gmail.com"

    seller = {
            "id" : 1,
            "email" : "hamdankhalid@gmail.com"
    }

    product = Products()
    product.id = 2
    product.name = "Hair Shampoo"
    product.price = 600
    product.seller_id = 1
    product.status = "Available"

    update_data = UpdateProduct(price=650)

    with patch(
        "app.services.product_service.get_seller_from_token", return_value=db_seller
    ) as mock_get_seller:

        with patch(
            "app.services.product_service.find_product_in_database", return_value=product
        ) as mock_get_product_in_database:
            
            with patch(
            "app.services.product_service.find_seller_product_in_database", return_value=product
        ) as mock_get_seller_product_in_database:
                              
               with patch(
                   "app.services.product_service.delete_seller_products_in_cache"
                ) as mock_delete_products_in_cache:

                    with pytest.raises(
                        exceptions.DatabaseError
                    ):
                        update_seller_product_attributes(2, update_data, seller, session)                

    mock_get_seller.assert_called_once_with(seller, session)
    mock_get_product_in_database.assert_called_once_with(2, session)
    mock_get_seller_product_in_database.assert_called_once_with(2, seller["id"], session)
    mock_delete_products_in_cache.assert_not_called()

    assert product.price == 650

    session.add.assert_called_once_with(product)
    session.commit.assert_not_called()

