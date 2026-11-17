from app.database_models.user_model import CreateUser
from app.database_models.user_model import Users
from app.services.user_service import IntegrityError

def test_create_user_valid_input():
    user = CreateUser(
        name="Hamdan Khalid",
        age=20,
        phone_number="03190286038",
        city="Karachi",
        email="hamdan@gmail.com",
        password="Hello12345"
    )

    assert user.name == "Hamdan Khalid"
    assert user.age == 20
    assert user.email == "hamdan@gmail.com"


import pytest
from pydantic import ValidationError

def test_create_user_invalid_age():

    with pytest.raises(ValidationError):
        CreateUser(
            name="Hamdan Khalid",
            age=5,
            phone_number="03190286038",
            city="Karachi",
            email="hamdan@gmail.com",
            password="Hello12345"
        )

def test_create_user_invalid_phone_no():

    with pytest.raises(ValidationError):
        CreateUser(
            name="Hamdan Khalid",
            age=50,
            phone_number="0319028608",
            city="Karachi",
            email="hamdan@gmail.com",
            password="Hello12345"
        )

def test_create_user_invalid_password_len():

    with pytest.raises(ValidationError):
        CreateUser(
            name="Hamdan Khalid",
            age=50,
            phone_number="03190286038",
            city="Karachi",
            email="hamdan@gmail.com",
            password="Heliwy"
        )

def test_create_user_invalid_email(session):

    new_user = Users(
        name="Abu Bakar",
        age=44,
        phone_number="03190286038",
        city="Karachi",
        email="hamdan@gmail.com",
        password="Hello2726#@"
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    with pytest.raises(ValidationError):
        CreateUser(
            name="Hamdan Khalid",
            age=50,
            phone_number="03190286038",
            city="Karachi",
            email="hamdan@gmail.com",
            password="Heliwy"
        )

