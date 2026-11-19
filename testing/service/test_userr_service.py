from app.services.user_service import create_user_account, login_user_by_email
from unittest.mock import Mock, patch
from app.database_models.user_model import Users, LoginUser
import pytest
from app.core import exceptions
from app.utils.password_hash import pwd_context, create_hash_password
from app.core import exceptions
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch

fk_db = Mock()

def test_create_new_user_account_but_user_already_exist(session):
    user = Users(
        name="Abu Bakar",
        age=44,
        phone_number="03190286038",
        city="Karachi",
        email="abubakar@gmail.com",
        password="Hello2726#@"
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    new_user = Users(
        name="Hamdan",
        age=20,
        phone_number="03263525252",
        city="Karachi",
        email="abubakar@gmail.com",
        password="Dijitize1646$!!@"
    )

    with pytest.raises(exceptions.UserAlreadyExist) as exc_info:
        create_user_account(new_user, session)

    assert str(exc_info.value) == "Account already exists at your email!"


def test_user_account_return_output(session):
    new_user = Users(
        name="Abu Bakar",
        age=44,
        phone_number="03190286038",
        city="Karachi",
        email="abubakar@gmail.com",
        password="Hello2726#@"
    )
    result = create_user_account(new_user, session)

    assert result.name == new_user.name
    assert result.age == new_user.age
    assert result.phone_number == new_user.phone_number
    assert result.city == new_user.city
    assert result.email == new_user.email
    assert pwd_context.verify(new_user.password, result.password) is True


def test_user_account_duplicate_error(session):
    user = Users(
        name="Abu Bakar",
        age=44,
        phone_number="03190286038",
        city="Karachi",
        email="abubakar@gmail.com",
        password="Hello2726#@"
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user = Users(
        name="Abu Bakar",
        age=44,
        phone_number="03190286038",
        city="Karachi",
        email="abubakar11@gmail.com",
        password="Hello2726#@"
    )

    with pytest.raises(exceptions.DuplicateUserData):
        create_user_account(user, session)


def test_user_account_but_database_error(session):
    user = Users(
        name="Abu Bakar",
        age=44,
        phone_number="03190286038",
        city="Karachi",
        email="abubakar@gmail.com",
        password="Hello2726#@"
    )

    with patch("app.services.user_service.new_user_save_in_database",
               side_effect=SQLAlchemyError("Database Error while created user account!")
               ):
        with pytest.raises(exceptions.DatabaseError):
            create_user_account(user, session) 


# def test_login_user_with_wrong_email(session, monkeypatch):

#     fake_get_user = Mock(return_value=None)

#     monkeypatch.setattr(
#         user_service,
#         "get_logged_in_user_by_email",
#         fake_get_user
#     )

#     user = LoginUser(
#         email="wrong@gmail.com",
#         password="password123"
#     )

#     with pytest.raises(exceptions.InvalidCredentials):
#         user_service.login_user_by_email(user, session)

#     fake_get_user.assert_called_once_with(user, session)

def test_login_user_with_incorrect_email(session):
    user = LoginUser(
        email="hamdan@gmail.com",
        password="Bismillahagsg"
    )

    with patch(
        "app.services.user_service.get_logged_in_user_by_email"
    ) as fake_user:

        fake_user.return_value = None

        with pytest.raises(
            exceptions.InvalidCredentials
        ):
            result = login_user_by_email(fake_user, session)
            assert result is None
            fake_user.assert_called_once_with(user, session)


def test_test_login_user_with_incorrect_password(session):

    user_login = LoginUser(
            email="abubakar@gmail.com",
            password="Hello2shs#@"
    )

    user = Users(
        name="Abu Bakar",
        age=44,
        phone_number="03190286038",
        city="Karachi",
        email="abubakar@gmail.com",
        password=create_hash_password("Hello2726#@")
    )

    with patch("app.services.user_service.get_logged_in_user_by_email") as fake_user:
        fake_user.return_value = user

        with pytest.raises(exceptions.InvalidCredentials):
            login_user_by_email(user_login, session)


def test_login_user_with_database_error(session):
    user_login = LoginUser(
            email="abubakar@gmail.com",
            password="Hello2shs#@"
    )

    with patch("app.services.user_service.get_logged_in_user_by_email",
               side_effect = SQLAlchemyError(
                   "Database Error during admin login!")
               ):
        with pytest.raises(exceptions.DatabaseError):
            login_user_by_email(user_login, session)

def test_user_login_successfully(session):
    user = Users(
        name="Abu Bakar",
        age=44,
        phone_number="03190286038",
        city="Karachi",
        email="abubakar@gmail.com",
        password=create_hash_password("Hello2726#@")
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user_login = LoginUser(
            email="abubakar@gmail.com",
            password="Hello2726#@"
    )

    result = login_user_by_email(user_login, session)

    assert result["access_token"] is not None
    assert result["token_type"] == "Bearer"
    