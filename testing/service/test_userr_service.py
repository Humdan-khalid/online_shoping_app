from app.services.user_service import create_user_account
from unittest.mock import Mock
from app.database_models.user_model import Users
import pytest
from app.core import exceptions
from app.utils.password_hash import pwd_context


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