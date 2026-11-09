from app.database_models.admin_model import Admin, CreateAdmin, AdminLogin
from sqlmodel import Session
from app.repository.admin_repo import get_admin_in_database_by_email, find_admin_by_email
from app.core import exceptions
from app.core.log_config import logging
from app.utils.password_hash import verify_password, create_hash_password
from app.core.jwt_token import create_token
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def create_admin_account(admin: CreateAdmin, session: Session):
    db_admin = get_admin_in_database_by_email(admin.email, session)

    if db_admin:
        logging.warning(f"Admin account already exist with this email | {admin.email}")
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

    except IntegrityError:
        session.rollback()
        logging.exception("User creation failed because of duplicate or invalid database data.")
        raise exceptions.DuplicateAdminData("Admin creation failed because of duplicate or invalid database data.")

    except SQLAlchemyError:

        session.rollback()

        logging.exception("Database error while creating admin.")

        raise exceptions.DatabaseError("Database Error!")
    

def admin_login_by_email_and_password(admin: AdminLogin, session: Session):
    try:
        db_admin = find_admin_by_email(admin.email, session)

    except SQLAlchemyError as error:
        session.rollback()

        logging.exception("Database Error during admin login!")

        raise exceptions.DatabaseError(
            "Database Error!"
        ) from error
        
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