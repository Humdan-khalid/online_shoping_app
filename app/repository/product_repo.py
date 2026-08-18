from app.database_models.product_model import CreateProduct, Products
from sqlmodel import Session, select
from app.database_models.seller_model import Sellers

def product_save_in_database(product: CreateProduct, session: Session):
    session.add(product)
    session.commit()
    session.refresh(product)

def find_product_in_database(product_id: int, session: Session):
    db_product = session.exec(
        select(Products).where(
            Products.id == product_id
        )).first()

    return db_product

def find_seller_product_in_database(product_id: int, seller_id: int, session: Session):
    db_product = session.exec(
        select(Products).where(
            Products.id == product_id,
            Products.seller_id == seller_id
        )
    ).first()

    return db_product

def find_seller_products_in_database(seller_id: int, session: Session):
    db_products = session.exec(
        select(Products).where(
                Products.seller_id == seller_id
        )
    ).all()

    return db_products


def get_products(search: str, session: Session):
    db_products = session.exec(select(Products).
                        where(Products.name.ilike(
                            f"%{search}%"
                        ))).all()

    return db_products

def find_seller_product_with_id(product_id: int, seller_id: int, session: Session):
    db_product = session.exec(
                    select(Products).where(
                            Products.seller_id == seller_id, 
                            Products.id == product_id
                    )
    ).first()

    return db_product

def find_product_with_id(product_id: int, session: Session):
    db_product = session.exec(
        select(Products).where(
            Products.id == product_id
        )
    ).first()

    return db_product
