
def test_create_user(client):
    response = client.post(
        "/users",
        json = {
            "name": "Hamdan",
            "age": 22,
            "phone_number": "03001234887",
            "city": "Karachi",
            "email": "hamdan87@gmail.com",
            "password": "12345678"
        
        }
    )


    assert response.status_code == 201

def test_create_user_with_existing_email(client):
    response = client.post(
        "/users",
        json = {
            "name": "Hamdan",
            "age": 22,
            "phone_number": "03001234887",
            "city": "Karachi",
            "email": "hamdan87@gmail.com",
            "password": "12345678"
        }
    )

    data = response.json()

    assert response.status_code == 409
    assert data['detail'] == "Account already exist at your email"


def test_create_user_without_password(client):
    response = client.post(
        "/users",
        json = {
            "name": "Hamdan",
            "age": 22,
            "phone_number": "03001234887",
            "city": "Karachi",
            "email": "hamdan87@gmail.com"
        }
    )

    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "password"]
    
    assert response.status_code == 422


def test_create_user_with_wrong_phone_number(client):
    response = client.post(
        "/users",
        json = {
            "name": "Hamdan",
            "age": 22,
            "phone_number": "03001234",
            "city": "Karachi",
            "email": "hamdan997@gmail.com",
            "password": "helor63535"
        }
    )

    data = response.json()

    assert data["detail"][0]["loc"] == ["body", "phone_number"]
    assert response.status_code == 422

def test_create_user_with_wrong_name(client):
    response = client.post(
        "/users",
        json = {
            "name": "1254",
            "age": 22,
            "phone_number": "03001234177",
            "city": "Karachi",
            "email": "hamdan997@gmail.com",
            "password": "helor63535"
        }
    )

    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "name"]

    assert response.status_code == 422

def test_create_user_with_wrong_age(client):
    response = client.post(
        "/users",
        json = {
            "name": "Bilal",
            "age": 9,
            "phone_number": "03001234177",
            "city": "Karachi",
            "email": "hamdan997@gmail.com",
            "password": "helor63535"
        }
    )

    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "age"]

    assert response.status_code == 422

def test_create_user_with_wrong_city(client):
    response = client.post(
        "/users",
        json = {
            "name": "Bilal",
            "age": 90,
            "phone_number": "03001234177",
            "city": "1737",
            "email": "hamdan997@gmail.com",
            "password": "helor63535"
        }
    )

    data = response.json()

    assert data["detail"][0]["loc"] == ["body", "city"]
    assert response.status_code == 422

def test_create_user_with_wrong_email(client):
    response = client.post(
        "/users",
        json = {
            "name": "Bilal",
            "age": 90,
            "phone_number": "03001234177",
            "city": "Karachi",
            "email": "hamdan997com",
            "password": "helor63535"
        }
    )


    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "email"]
    assert response.status_code == 422
