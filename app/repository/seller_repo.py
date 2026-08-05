from app.database_models.seller_model import Sellers, CreateSeller, SellerLogin
from sqlmodel import Session, select


def find_seller_to_email(seller: CreateSeller, session: Session):
    db_seller = session.exec(
            select(Sellers).where(
                Sellers.email == seller.email)
                ).first()

    return db_seller

def seller_data_save_in_database(seller: CreateSeller, session: Session):
        session.add(seller)
        session.commit()
        session.refresh(seller)

def find_seller_for_login(seller: SellerLogin, session: Session):
      db_seller = session.exec(
                    select(Sellers).where(
                        Sellers.email == seller.email)).first()

      return db_seller

def find_seller_in_database(seller_id: int, session: Session):
    db_seller = session.exec(
                    select(Sellers).where(
                        Sellers.id == seller_id
                    )
    ).first()

    return db_seller