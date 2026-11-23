from app.services.seller_service import create_new_seller_account, seller_account_login
from app.database_models.seller_model import Sellers, CreateSeller, SellerLogin
from unittest.mock import patch
import pytest
from app.core import exceptions
from sqlalchemy.exc import SQLAlchemyError
from app.utils.password_hash import create_hash_password

def test_create_seller_account_but_email_exist(session):
    new_seller = Sellers(
        name="Alia Sohail",
        age=30,
        phone_number="03123838448",
        city="London",
        email="aliasohial222@gmail.com",
        password="Hello1232"
    )

    with patch("app.services.seller_service.find_seller_to_email",
               return_value = new_seller):
        with pytest.raises(exceptions.SellerAlreadyExist) as exc_info:
            result = create_new_seller_account(new_seller, session)

            assert exc_info['detail'] == "Seller account already exist at email."
            assert result.email == "aliasohial222@gmail.com"


def test_create_seller_account_duplicate_phone_num_error(session):
    seller = Sellers(
        name="Alia Sohail",
        age=30,
        phone_number="03123838448",
        city="London",
        email="aliasohial222@gmail.com",
        password="Hello1232"
    )

    session.add(seller)
    session.commit()
    session.refresh(seller)

    new_seller = Sellers(
        name="Alia",
        age=20,
        phone_number="03123838448",
        city="London",
        email="aliasohial343@gmail.com",
        password="Hello1232"
    )

    with pytest.raises(exceptions.DuplicateSellerData):
        create_new_seller_account(new_seller, session)


def test_create_seller_account_database_error(session):
    new_seller = CreateSeller(
        name="Alia",
        age=20,
        phone_number="03123838448",
        city="London",
        email="aliasohial343@gmail.com",
        password="Hello1232"
    )

    with patch("app.services.seller_service.seller_data_save_in_database",
               side_effect=SQLAlchemyError("Database Error!")
               ):
        with pytest.raises(exceptions.DatabaseError):
            create_new_seller_account(new_seller, session)


def test_seller_created_successfully(session):
    new_seller = CreateSeller(
        name="Alia",
        age=20,
        phone_number="03123838448",
        city="London",
        email="aliasohial343@gmail.com",
        password="Hello1232"
    )

    result = create_new_seller_account(new_seller, session)

    assert result.name == "Alia"
    assert result.email == "aliasohial343@gmail.com"

def test_seller_not_found_to_email(session):
    seller = SellerLogin(
        email= "hamdankhalid663@gmail.com",
        password= "Bismillah2830"
    )

    with pytest.raises(exceptions.InvalidCredentials) as exc_info:
        seller_account_login(seller, session)
    assert str(exc_info.value) == "Email not found when seller was tried for login."

def test_seller_not_found_to_password(session):
    seller = Sellers(    
        name="Hamdan Khalid",
        age=22,
        phone_number="03292938383",
        city="Karachi",
        email="hamdankhalid663@gmail.com",
        password=create_hash_password("Hello1232")
        )

    session.add(seller)
    session.commit()
    session.refresh(seller)

    seller_login = SellerLogin(
        email= "hamdankhalid663@gmail.com",
        password= "Bismillah2830"
    )

    with pytest.raises(exceptions.InvalidCredentials) as exc_info:
        seller_account_login(seller_login, session)
    assert str(exc_info.value) == "Password not found when seller was tried for login."

def test_seller_login_database_error(session):
    seller = Sellers(    
        name="Hamdan Khalid",
        age=22,
        phone_number="03292938383",
        city="Karachi",
        email="hamdankhalid663@gmail.com",
        password=create_hash_password("Hello1232")
        )

    session.add(seller)
    session.commit()
    session.refresh(seller)

    seller_login = SellerLogin(
        email= "hamdankhalid663@gmail.com",
        password= "Hello1232"
    )

    with patch(
        "app.services.seller_service.find_seller_for_login",
        side_effect=SQLAlchemyError
    ):
        with pytest.raises(exceptions.DatabaseError) as exc_info:
            seller_account_login(seller_login, session)

    assert str (exc_info.value) == "Database Error!"

def test_seller_login_successfully(session):
    seller = Sellers(    
        name="Hamdan Khalid",
        age=22,
        phone_number="03292938383",
        city="Karachi",
        email="hamdankhalid663@gmail.com",
        password=create_hash_password("Hello1232")
        )

    session.add(seller)
    session.commit()
    session.refresh(seller)

    seller_login = SellerLogin(
        email= "hamdankhalid663@gmail.com",
        password= "Hello1232"
    )

    result = seller_account_login(seller_login, session)

    assert result["access_token"] is not None
    assert result["token_type"] == "Bearer"