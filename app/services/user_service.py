from app.database_models.user_model import CreateUser, Users, LoginUser
from sqlmodel import Session
from app.repository.user_repo import get_user_by_email_in_database , get_logged_in_user_by_email, new_user_save_in_database
from app.core import exceptions
from app.core.log_config import logger
from sqlalchemy.exc import DatabaseError
from app.utils.password_hash import create_hash_password, verify_password
from app.core.jwt_token import create_token
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def create_user_account(user: CreateUser, session: Session):
    try:
        user_exist = get_user_by_email_in_database(user, session)

        if user_exist:
            logger.warning(f"User account already exists at this email | {user.email}")
            raise exceptions.UserAlreadyExist("Account already exists at your email!")
    
        new_user = Users(
            name=user.name,
            age=user.age,
            phone_number=user.phone_number,
            city=user.city,
            email=user.email,
            password=create_hash_password(user.password)
        )
        
        new_user_save_in_database(new_user, session)
        
        logger.info(f"Successfully new user account created with this email | {user.email}")
        return new_user

    except IntegrityError:
        session.rollback()
        logger.exception("User creation failed because of duplicate or invalid database data.")

        raise exceptions.DuplicateUserData("duplicate or invalid database data!")

    except SQLAlchemyError:
        session.rollback()
        logger.exception("Database Error while created user account!")
        raise exceptions.DatabaseError(
            "Database Error!"
        )
    

def login_user_by_email(user: LoginUser, session: Session):
    try:
        db_user = get_logged_in_user_by_email(user, session)

    except SQLAlchemyError as error:
        session.rollback()
        logger.exception("Database Error during admin login!")
        raise exceptions.DatabaseError("Database Error!") from error    

    if not db_user:
        logger.warning(f"User login failed with wrong email | {user.email}")
        raise exceptions.InvalidCredentials("User email not found")
    
    db_password = verify_password(user.password, db_user.password)
    
    if not db_password:
        logger.warning(f"User login failed with wrong password | {user.password}")
        raise exceptions.InvalidCredentials("User password incorrect!")
        
    token = create_token(
        {
            "id": db_user.id,
            "email":db_user.email
        }
    )
    logger.info(f"User successfully login | user_id: {db_user.id}.")

    return{
        "access_token": token,
        "token_type": "Bearer"
        }

