from sqlmodel import Session
from app.core import exceptions
from app.repository.user_repo import get_user_by_id
from app.repository.product_repo import find_product_with_product_id
from app.database_models.cart_model import Cart
from sqlalchemy.exc import SQLAlchemyError
from app.core.log_config import logger


def get_user_for_cart(product_id:int, quantity: int, user_id:int, session: Session):
    try:
        user = get_user_by_id(user_id, session)

        if not user:
            logger.warning("User try to added the product in cart but user not found!")
            raise exceptions.UserNotFound("User not found!")

        product = find_product_with_product_id(product_id, session)

        if not product:
            logger.warning("User try to added the product in cart but product not found!")
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

        logger.info("Successfully Product added in cart.")
        return cart
    
    except SQLAlchemyError as error:
        logger.exception("Database error while user add the product in cart.")
        session.rollback()
        raise exceptions.DatabaseError(
            "Database Error!"
        ) from error