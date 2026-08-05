from app.repository.user_repo import get_user_by_email_in_database, get_logged_in_user_by_email
from app.database_models.user_model import Users, LoginUser

def test_user_find_by_email(db_session):

    new_user = Users(
        name="Ahmad Raza",
        age=23,
        phone_number="03122938484",
        city="Melbourne",
        email="ahmad@gmail.com",
        password="Hekdifj212"
    )

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    user = get_user_by_email_in_database(new_user, db_session)

    assert user is not None

def test_user_not_find_by_email(db_session):

    new_user = Users(
        name="Sawera Noor",
        age=19,
        phone_number="003162626373",
        city="Sialkot",
        email="sawera@gmail.com",
        password="Hsgstteg46"
    )


    user = get_user_by_email_in_database(new_user, db_session)

    assert user is None

def test_find_user_by_id(db_session):

    user = Users(
        name="Muhammad",
        age=29,
        phone_number="03152535355",
        city="Abbotabad",
        email="muhammad@gmail.com",
        password="Hsgsre3442"
    )

    db_session.add(user)
    db_session.commit()

    user_login =LoginUser(
        email="muhammad@gmail.com",
        password="Hsgsre3442"
    )

    user = get_logged_in_user_by_email(user_login, db_session)

    assert user is not None

def test_user_not_found_by_id(db_session):

    user_login =LoginUser(
        email="muhammad1@gmail.com",
        password="Hsgsre3442"
    )

    user = get_logged_in_user_by_email(user_login, db_session)

    assert user is None