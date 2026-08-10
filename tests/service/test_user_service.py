from app.services.user_service import login_user_by_email
from app.database_models.user_model import Users, LoginUser
import pytest
from app.core import exceptions
from app.utils.password_hash import create_hash_password
from app.services.user_service import create_user_account


def test_user_account_not_found_for_login(db_session):

    user_login = LoginUser(
        email="fatima@gmail.com",
        password="Hekdifj212"
    )

    with pytest.raises(exceptions.InvalidCredentials):
        login_user_by_email(user_login, db_session)


def test_invalid_user_password_for_login(db_session):
    new_user = Users(
        name="Fatima Khalid",
        age=23,
        phone_number="03122938484",
        city="New York",
        email="fatima@gmail.com",
        password=create_hash_password("Hekdifj212")
    )

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    user_login = LoginUser(
        email="fatima@gmail.com",
        password="Hekdahj212"
    )

    with pytest.raises(exceptions.InvalidCredentials):
        login_user_by_email(user_login, db_session)


def test_user_login_successfully(db_session):
    new_user = Users(
        name="Fatima Khalid",
        age=23,
        phone_number="03122938484",
        city="New York",
        email="fatima122@gmail.com",
        password=create_hash_password("Hekdifj212")
    )

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    user_login = LoginUser(
        email="fatima122@gmail.com",
        password="Hekdifj212"
    )

    user = login_user_by_email(user_login, db_session)

    assert "access_token" in user
    assert user['token_type'] == "Bearer"


def test_create_user_account_with_existing_email(db_session):
    existing_user = Users(
        name="Ahmad Raza",
        age=23,
        phone_number="03122938484",
        city="Melbourne",
        email="ahmad123@gmail.com",
        password="Hekdifj212"
    )

    db_session.add(existing_user)
    db_session.commit()
    db_session.refresh(existing_user)

    new_user = Users(
        name="Ahmad Raza",
        age=23,
        phone_number="03122938484",
        city="Melbourne",
        email="ahmad123@gmail.com",
        password="Hekdifj212"
    )

    with pytest.raises(exceptions.UserAlreadyExist):
        create_user_account(new_user, db_session)


def test_create_user_account(db_session):
    new_user = Users(
        name="Ahmad Raza",
        age=23,
        phone_number="03122938484",
        city="Melbourne",
        email="ahmad12333@gmail.com",
        password="Hekdifj212"
    )

    create_user_account(new_user, db_session)

