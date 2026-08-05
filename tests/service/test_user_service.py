import pytest
from app.core import exceptions
from app.services.user_service import create_user_account
from app.database_models.user_model import Users

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

