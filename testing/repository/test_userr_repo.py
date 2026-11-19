from app.repository.user_repo import get_user_by_email_in_database, new_user_save_in_database, get_logged_in_user_by_email
from app.database_models.user_model import Users, LoginUser
from sqlmodel import select

def test_user_not_found_by_email_in_database(session):
    user = Users(
        name="Hamdan",
        age=20,
        phone_number="03190286038",
        city="Karachi",
        email="hamdan@gmail.com",
        password="Bismiaia4646"
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    result = get_user_by_email_in_database(user.email, session)

    assert result is not None
    assert result.email == "hamdan@gmail.com"
    assert result.name == "Hamdan"


def test_user_found_by_email_in_database(session):
    new_user = Users(
        email="hamdan@gmail.com",
        )

    result = get_user_by_email_in_database(new_user.email, session)

    assert result == None


def test_new_user_save_in_database(session):
    user = Users(
        name="Hamdan",
        age=20,
        phone_number="03190286038",
        city="Karachi",
        email="hamdan@gmail.com",
        password="Bismiaia4646"
    )
    new_user_save_in_database(user, session)

    get_user = session.exec(
        select(Users).where(
            Users.email == user.email
        )
    ).first()

    assert get_user is not None
    assert get_user.name == "Hamdan"
    assert get_user.phone_number == "03190286038"

def test_get_user_for_logged_in(session):
    user = Users(
        name="Hamdan",
        age=20,
        phone_number="03190286038",
        city="Karachi",
        email="hamdan@gmail.com",
        password="Bismiaia4646"
    )
    new_user_save_in_database(user, session)

    db_user = LoginUser(
        email="hamdan@gmail.com",
        password="Bismiaia4646"
    )

    result = get_logged_in_user_by_email(db_user, session)

    assert result is not None
    assert result.name == "Hamdan"
    assert result.email == "hamdan@gmail.com"

def test_user_not_found_for_login(session):
    db_user = LoginUser(
        email="hamdan33@gmail.com",
        password="Bismiaia4646"
    )

    result = get_logged_in_user_by_email(db_user, session)
    assert result == None



