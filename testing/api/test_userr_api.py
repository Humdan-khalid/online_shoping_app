from app.api.user_api  import create_user_new_account
from app.core import exceptions

def test_create_new_user_account(client):
    new_user = {
        "name": "Hamdan",
        "age": 20,
        "phone_number": "03190286038",
        "city": "karachi",
        "email": "hamdan@gmail.com",
        "password": "Grieund211"
    }

    response = client.post("/users/", json=new_user)
    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Hamdan"
    assert data["age"] == 20
    assert data["city"] == "karachi"
    assert data["email"] == "hamdan@gmail.com"
    assert data["phone_number"] == "03190286038"
    assert "id" not in data
    assert "password" not in data

def test_create_new_user_account_but_user_already_exist(client):
    new_user = {
        "name": "Hamdan",
        "age": 20,
        "phone_number": "03190286038",
        "city": "karachi",
        "email": "hamdan@gmail.com",
        "password": "Grieund211"
    }

    response = client.post("/users/", json=new_user)
    assert response.status_code == 201

    response = client.post("/users/", json=new_user)
    assert response.status_code == 409

    data = response.json()

    assert data["detail"] == "An account with this email already exists."

def test_create_new_user_account_but_user_duplicate_phone_no(client):
    new_user = {
        "name": "Hamdan",
        "age": 20,
        "phone_number": "03190286038",
        "city": "karachi",
        "email": "hamdan122@gmail.com",
        "password": "Grieund211"
    }

    response = client.post("/users/", json=new_user)
    assert response.status_code == 201

    duplicate_phone_no = {
        "name": "Hamdan",
        "age": 20,
        "phone_number": "03190286038",
        "city": "karachi",
        "email": "hamdan@gmail.com",
        "password": "Grieund211"
    }

    response = client.post("/users/", json=duplicate_phone_no)
    assert response.status_code == 409

    data = response.json()

    assert data["detail"] == "Phone number or email already exists!"


from unittest.mock import patch


def test_create_user_but_database_error(client):

    new_user = {
        "name": "Hamdan",
        "age": 20,
        "phone_number": "03190286038",
        "city": "Karachi",
        "email": "hamdan@gmail.com",
        "password": "Grieund211"
    }

    with patch(
        "app.api.user_api.create_user_account",
        side_effect=exceptions.DatabaseError("Database Error!")
    ):

        response = client.post("/users/", json=new_user)

    assert response.status_code == 500

    data = response.json()

    assert data["detail"] == "Internal Server Error!"

def test_user_login_but_database_error(client):
    user =  {
            "email": "hamdan@gmail.com",
            "password": "Grieund211"
        }

    with patch(
        "app.api.user_api.login_user_by_email",
        side_effect = exceptions.DatabaseError
    ):
        response = client.post("/user-login", json=user)

        assert response.status_code == 500

        message = response.json()

        assert message["detail"] == "Internal Server Error!"
        
def test_user_login_but_invalid_email(client):
    user =  {
            "email": "hamdan@gmail.com",
            "password": "Grieund211"
        }

    with patch(
        "app.api.user_api.login_user_by_email",
        side_effect = exceptions.InvalidCredentials
    ):
        response = client.post("/user-login", json=user)

        assert response.status_code == 404

        message = response.json()

        assert message["detail"] == "Invalid email or password!"

def test_user_login_but_password_not_found(client):
    user =  {
            "email": "hamdan@gmail.com",
            "password": "Grieund211"
        }

    with patch(
        "app.api.user_api.login_user_by_email",
        side_effect = exceptions.InvalidCredentials
    ):
        response = client.post("/user-login", json=user)

        assert response.status_code == 404

        message = response.json()

        assert message["detail"] == "Invalid email or password!"