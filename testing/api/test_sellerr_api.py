from unittest.mock import patch
from app.core import exceptions
from app.database_models.seller_model import CreateSeller, SellerLogin, Sellers
from app.utils.password_hash import create_hash_password

def test_create_seller_but_seller_exist(client):
    new_seller = CreateSeller(
        name="Alia",
        age=20,
        phone_number="03123838448",
        city="London",
        email="aliasohial343@gmail.com",
        password="Hello1232"
    )
    with patch("app.api.seller_api.create_new_seller_account",
               side_effect=exceptions.SellerAlreadyExist("Seller already exists")):
        
        result = client.post("/sellers", json=new_seller.model_dump())
        assert result.status_code == 409
        assert result.json()["detail"] == "A seller account already exists with this email!"



def test_create_seller_but_phone_no_exist(client):
    new_seller = CreateSeller(
        name="Alia",
        age=20,
        phone_number="03123838448",
        city="London",
        email="aliasohial343@gmail.com",
        password="Hello1232"
    )
    with patch("app.api.seller_api.create_new_seller_account",
               side_effect=exceptions.DuplicateSellerData("Seller already exists")):
        
        result = client.post("/sellers", json=new_seller.model_dump())
        assert result.status_code == 409
        assert result.json()["detail"] == "Phone number or email already exists!"

def test_create_seller_account_successfully(client):
    new_seller = CreateSeller(
        name="Alia",
        age=20,
        phone_number="03123838448",
        city="London",
        email="aliasohial343@gmail.com",
        password="Hello1232"
    )

    result = client.post("/sellers", json=new_seller.model_dump())
    assert result.status_code == 201
    assert result.json()["name"] == "Alia"
    assert result.json()["phone_number"] == "03123838448"
    assert result.json()["email"] == "aliasohial343@gmail.com"
    assert "password" not in result.json()

def test_seller_not_found_with_invalid_email(client):
    seller = SellerLogin(
        email="hamdan@gmail.com",
        password="Bismillah2830"
    )

    data = client.post("/seller-login", json=seller.model_dump())
    result = data.json()
    assert data.status_code == 409
    assert result["detail"] == "Invalid email or password!"


def test_seller_not_found_with_invalid_password(client, session):
    new_seller = Sellers(
        name="Hamdan",
        age=27,
        city="Karachi",
        phone_number="03122838499",
        email="hamdan@gmail.com",
        password=create_hash_password("WebDev$:111")
    )

    session.add(new_seller)
    session.commit()
    session.refresh(new_seller)

    seller = SellerLogin(
        email="hamdan@gmail.com",
        password="Bismillah2830"
    )

    data = client.post("/seller-login", json=seller.model_dump())
    result = data.json()
    assert data.status_code == 409
    assert result["detail"] == "Invalid email or password!"

def test_seller_login_successfully(client, session):
    new_seller = Sellers(
        name="Hamdan",
        age=27,
        city="Karachi",
        phone_number="03122838499",
        email="hamdan@gmail.com",
        password=create_hash_password("WebDev$:111")
    )

    session.add(new_seller)
    session.commit()
    session.refresh(new_seller)

    seller = SellerLogin(
        email="hamdan@gmail.com",
        password="WebDev$:111"
    )

    data = client.post("/seller-login", json=seller.model_dump())
    result = data.json()

    assert data.status_code == 200
    assert result["access_token"] is not None
    assert result["token_type"] == "Bearer"
    