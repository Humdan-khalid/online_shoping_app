from app.services.user_service import login_user_by_email
from app.database_models.user_model import Users, LoginUser
import pytest
from app.core import exceptions
from app.utils.password_hash import create_hash_password, verify_password

def test_user_account_not_found_for_login(db_session):

    user_login = LoginUser(
        email="fatima@gmail.com",
        password="Hekdifj212"
    )

    with pytest.raises(exceptions.InvalidCredentials):
        login_user_by_email(user_login, db_session)


def test_user_password_invalid_for_login(db_session):
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


def test_user_login_success(db_session):
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