from app.database_models.admin_model import Admin, CreateAdmin, AdminLogin
from sqlmodel import Session
from app.repository.admin_repo import get_admin_in_database_by_email, admin_login_by_email
from app.core import exceptions
from sqlalchemy.exc import DatabaseError
from app.core.log_config import logging
from app.utils.password_hash import verify_password, create_hash_password
from app.core.jwt_token import create_token

def create_admin_account(admin: CreateAdmin, session: Session):
    db_admin = get_admin_in_database_by_email(admin, session)

    if db_admin:
        logging.warning(f"Admin account already exist with email | {admin.email}")
        raise exceptions.AdminAlreadyExist("Admin already exist in database.")

    try:
        new_admin = Admin(
            name= admin.name,
            age=admin.age,
            city=admin.city,
            phone_number=admin.phone_number,
            email=admin.email,
            password=create_hash_password(admin.password)
        )

        session.add(new_admin)
        session.commit()
        session.refresh(new_admin)

        return new_admin

    except DatabaseError:
        logging.exception("Database error while admin created new account!")
        raise exceptions.DatabaseError("Database error!")
    

def admin_login_with_id(admin: AdminLogin, session: Session):
    try:
        db_admin = admin_login_by_email(admin, session)
        if not db_admin:
            logging.warning(f"Invalid admin trying to login to this email. | email: {admin.email}")
            raise exceptions.InvalidCredentials("Invalid email or password!")

        db_password = verify_password(admin.password, db_admin.password)

        if not db_password:
            logging.warning(f"Invalid admin trying to login to this password. | password: {admin.password}")
            raise exceptions.InvalidCredentials("Invalid email or password!")

        
        token = create_token(
            {"id": db_admin.id,
            "email": db_admin.email}
        )

        return{
            "token": token,
            "token_type": "Bearer"
        }


    except DatabaseError:
        logging.exception("Database error while admin tried to login!")
        raise exceptions.DatabaseError("Database error!")
