def test_get_products(client):
    user_data = {
        "name": "Hamdan",
        "age": 20,
        "phone_number": "03190286038",
        "city": "karachi",
        "email": "hamdan@gmail.com",
        "password": "Grieund211"
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201
