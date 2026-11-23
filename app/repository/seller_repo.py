from app.database_models.seller_model import Sellers, CreateSeller, SellerLogin
from sqlmodel import Session, select
from pydantic import EmailStr

def find_seller_to_email(email: EmailStr, session: Session):
    return session.exec(
            select(Sellers).where(
                Sellers.email == email)
                ).first()


def seller_data_save_in_database(seller: Sellers, session: Session):
        session.add(seller)
        session.commit()
        session.refresh(seller)

def find_seller_for_login(email: EmailStr, session: Session):
      return session.exec(
                    select(Sellers).where(
                        Sellers.email == email)).first()

def find_seller_in_database(seller_id: int, session: Session):
    db_seller = session.exec(
                    select(Sellers).where(
                        Sellers.id == seller_id
                    )
    ).first()

    return db_seller


def get_seller_from_token(seller: dict, session: Session)->Sellers | None:
    return session.exec(
        select(Sellers).where(
            Sellers.id == seller["id"],
            Sellers.email == seller["email"]   
            )
        ).first()