from sqlmodel import Session
from app.core import exceptions
from app.repository.user_repo import get_user_by_id
from app.repository.product_repo import find_product_with_id
from app.database_models.cart_model import Cart
from sqlalchemy.exc import DatabaseError
from app.core.log_config import logging


def get_user_for_cart(product_id:int, quantity: int, user_id:int, session: Session):
    try:
        user = get_user_by_id(user_id, session)

        if not user:
            raise exceptions.UserNotFound("User not found!")

        product = find_product_with_id(product_id, session)

        if not product:
            raise exceptions.ProductNotFound("Product not found!")

        cart = Cart(
            product_name=product.name,
            quantity=quantity,
            product_id=product.id,
            customer_id=user.id,
            seller_id=product.seller_id
        )

        session.add(cart)
        session.commit()
        session.refresh(cart)

        return cart
    
    except DatabaseError:
        logging.exception("Database Error! while user cart the product.")
        raise