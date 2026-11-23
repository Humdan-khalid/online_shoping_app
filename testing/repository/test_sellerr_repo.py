from app.repository.seller_repo import find_seller_to_email
from app.database_models.seller_model import Sellers, SellerLogin
from app.repository.seller_repo import find_seller_for_login, get_seller_from_token
from app.utils.password_hash import create_hash_password

def test_find_seller_to_email(session):
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

    result = find_seller_to_email(seller.email, session)

    assert result.name == "Alia Sohail"
    assert result.email == "aliasohial222@gmail.com"

def test_seller_not_found_to_email(session):
    seller = Sellers(
        name="Alia Sohail",
        age=30,
        phone_number="03123838448",
        city="London",
        email="aliasohial222@gmail.com",
        password="Hello1232"
    )
    result = find_seller_to_email(seller.email, session)

    assert result == None

def test_seller_email_not_found_for_login(session):
    seller = SellerLogin(
        email= "hamdankhalid663@gmail.com",
        password= "Bismillah2830"
    )

    result = find_seller_for_login(seller.email, session)
    assert result == None

def test_seller_email_found_successfully(session):
    seller = Sellers(
        name="Hamdan Khalid",
        age=20,
        phone_number="03190286038",
        city="Karachi",
        email="hamdankhalid663@gmail.com",
        password=create_hash_password("Bismillah2830")
    )

    session.add(seller)
    session.commit()
    session.refresh(seller)

    seller = SellerLogin(
        email= "hamdankhalid663@gmail.com",
        password= "Bismillah2830"
    )

    result = find_seller_for_login(seller.email, session)
    assert result.name == "Hamdan Khalid"
    assert result.email == "hamdankhalid663@gmail.com"
    
def test_seller_not_found_by_email_from_token(session):
    seller_login = {
        "id":1,
        "email":"hamdankhalid663@gmail.com",
        "password":("Bismillah2830")
    }

    result = get_seller_from_token(seller_login, session)

    assert result == None

def test_seller_found_by_email_from_token(session):
    seller = Sellers(
        name="Hamdan Khalid",
        age=20,
        phone_number="03190286038",
        city="Karachi",
        email="hamdankhalid663@gmail.com",
        password=create_hash_password("Bismillah2830")
    )

    session.add(seller)
    session.commit()
    session.refresh(seller)

    seller_login = {
        "id":1,
        "email":"hamdankhalid663@gmail.com",
        "password":("Bismillah2830")
    }

    result = get_seller_from_token(seller_login, session)

    assert result.email == "hamdankhalid663@gmail.com"
    assert result.phone_number == "03190286038"


