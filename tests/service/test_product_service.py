from app.services.product_service import create_new_product, update_seller_product_attributes, deactivate_seller_product, find_carts_in_database
from unittest.mock import patch, Mock
import pytest
from app.core import exceptions
from app.database_models.product_model import UpdateProduct, Products
from app.database_models.cart_model import Cart
from app.database_models.seller_model import Sellers
from app.database_models.user_model import Users

def test_create_product_but_seller_not_found():

    product = Mock()
    session = Mock()
    token = {
        "id": 1,
        "email": "hamdan@gmail.com"
    }

    with patch("app.services.product_service.get_seller_from_token", return_value=None) as fake_seller_verify:
        with pytest.raises(exceptions.UnauthorizedSeller):
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

def test_deactivate_product_but_seller_not_found():
    seller = {
        "id": 1,
        "email": "hamdan@gmail.com"
    }

    fake_session = Mock()

    with patch(
        "app.services.product_service.get_seller_from_token", return_value=None
    ) as mock_seller:
        with pytest.raises(
            exceptions.SellerNotExist
        ):
            deactivate_seller_product(2, seller, fake_session)
            
    mock_seller.assert_called_once_with(seller, fake_session)

def test_deactivate_product_but_product_not_found():
    fake_seller = {
        "id": 2,
        "email": "hamdan@gmail.com"
    }
    fake_session = Mock()

    with patch(
        "app.services.product_service.get_seller_from_token", return_value=fake_seller
    ) as mock_seller:
        with patch(
            "app.services.product_service.find_product_in_database", return_value=None
        ):
            with pytest.raises(
                exceptions.ProductNotFound
            ):
                deactivate_seller_product(2, fake_seller, fake_session)

                assert mock_seller.assert_called_once_with(fake_seller, fake_session)

def test_deactivate_product_but_seller_product_not_found():
    fake_seller = {
        "id": 2,
        "email": "hamdan@gmail.com"
    }

    fake_product = {
        "id": 1,
        "name": "Pizza Machine",
        "price": 30000.0
    }

    fake_session = Mock()

    with patch(
        "app.services.product_service.get_seller_from_token", return_value=fake_seller
    ) as mock_seller:

        with patch(
            "app.services.product_service.find_product_in_database", return_value=fake_product
            ) as mock_product:

            with patch(
                "app.services.product_service.find_seller_product_in_database", return_value = None
            ) as mock_seller_product:

                with pytest.raises(
                    exceptions.ProductNotFound
                ):

                    deactivate_seller_product(1, fake_seller, fake_session)

                    assert mock_seller.assert_called_once_with(fake_seller, fake_session)
                    assert mock_product.assert_called_once_with(fake_product['id'], fake_session)
                    assert mock_seller_product.assert_called_once_with(fake_product['id'], fake_seller, fake_session)


def test_deactivate_product_but_product_status_is_not_available():
    fake_seller = {
        "id": 2,
        "email": "hamdan@gmail.com"
    }

    fake_product = Mock()

    fake_product.id = 1
    fake_product.status = "Not Available"

    fake_session = Mock()

    with patch(
        "app.services.product_service.get_seller_from_token", return_value=fake_seller
    ) as mock_seller:

        with patch(
            "app.services.product_service.find_product_in_database", return_value=fake_product
            ) as mock_product:

            with patch(
                "app.services.product_service.find_seller_product_in_database", return_value = fake_product
            ) as mock_seller_product:

                with pytest.raises(
                    exceptions.ProductAlreadyInactivate
                ):

                    deactivate_seller_product(1, fake_seller, fake_session)

        mock_seller.assert_called_once_with(fake_seller, fake_session)
        mock_product.assert_called_once_with(1, fake_session)
        mock_seller_product.assert_called_once_with(1, fake_seller['id'], fake_session)


def test_deactivate_product_delete_in_cart(db_session):
    seller = Sellers(
        id= 2,
        name= "Hamdan Khalid",
        age= 21,
        phone_number=  "03484848484",
        city= "Karachi",
        email= "hamdan@gmail.com",
        password= "Hdg232$!"
    )

    db_session.add(seller)
    db_session.commit()

    user = Users(
        id= 1,
        name="Hamdan Khalid",
        age=34,
        phone_number="03123838488",
        city="Islamabad",
        email="hamdan@gmail.com",
        password="Gsudusudgd"
    )
    db_session.add(user)
    db_session.commit()

    product = Products(
        id=6,
        name="Shoes",
        price=3000,
        colour="Black",
        brand="Nike",
        description="Nike brand is very good for wearing.",
        seller_id=seller.id,
        quantity=29,
        weight="500gm",
        status="Available"
    )
    db_session.add(product)
    db_session.commit()

    db_seller = {
        "id": 2,
        "email": "hamdan@gmail.com"
    }

    cart1 = Cart(
        product_name="Face Cream",
        product_id=product.id,
        customer_id=user.id,
        seller_id=seller.id,
        quantity=20,
        status="Available"
    )

    db_session.add(cart1)
    db_session.commit()

    cart2 = Cart(
        product_name="Shampoo",
        product_id=product.id,
        customer_id=user.id,
        seller_id=seller.id,
        quantity=10,
        status="Available"
        )
    
    db_session.add(cart2)
    db_session.commit()

    deactivate_seller_product(6, db_seller, db_session)

    db_carts = find_carts_in_database(product.id, db_session)

    for cart in db_carts:
        db_session.delete(cart)

    assert db_carts == []

    db_session.commit()
    

