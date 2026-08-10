from app.repository.seller_repo import find_seller_to_email, seller_data_save_in_database, find_seller_for_login
from app.database_models.seller_model import CreateSeller, Sellers, SellerLogin
from app.core import exceptions
from sqlalchemy.exc import DatabaseError
from app.core.log_config import logging
from sqlmodel import Session
from app.utils.password_hash import verify_password, create_hash_password
from app.core.jwt_token import create_token

def create_new_seller_account(seller: CreateSeller, session: Session):

    try:
        db_seller = find_seller_to_email(seller, session)

        if db_seller:
            logging.warning(f"Seller account already exist at email. | {seller.email}")
            raise exceptions.InvalidCredentials("Seller account already exist at email.")

        new_seller = Sellers(
            name=seller.name,
            age=seller.age,
            phone_number=seller.phone_number,
            city=seller.city,
            email=seller.email,
            password=create_hash_password(seller.password)
        )

        seller_data_save_in_database(new_seller, session)
        return new_seller
    
    except DatabaseError:
        logging.exception("Database Error!")
        raise 


def seller_account_login(seller: SellerLogin, session: Session):
    try:
        seller_exist = find_seller_for_login(seller, session)

        if not seller_exist:
            logging.warning(f"Seller gave the invalid email for login. | Invalid_email: {seller.email}")
            raise exceptions.InvalidCredentials("Email not found when seller was tried for login.")

        seller_password_verify = verify_password(seller.password, seller_exist.password)

        if not seller_password_verify:
            logging.warning(f"Seller gave the invalid password for login. | Invalid_email: {seller.password}")
            raise exceptions.InvalidCredentials("Password not found when seller was tried for login.")

        token = create_token(
            {
                "id": seller_exist.id,
                "email": seller_exist.email
            }
        )

        return{
            "access_token": token,
            "token_type": "Bearer"    
        }

    except DatabaseError:
        logging.exception("Database error while seller tried for logging account.")
        raise 