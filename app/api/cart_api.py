from app.services.cart_service import get_user_for_cart
from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session
from app.database_config.database_connection import get_session
from app.core.jwt_token import get_user_token
from app.core import exceptions
from sqlalchemy.exc import DatabaseError

router = APIRouter()

@router.post("/cart_product", status_code=status.HTTP_201_CREATED)
def user_cart(product_id: int, quantity: int, user: dict = Depends(get_user_token), session: Session = Depends(get_session)):
    try:
        return get_user_for_cart(product_id, quantity, user['id'], session)
    except exceptions.UserNotFound:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User!")

    except exceptions.SellerNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")

    except DatabaseError:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error!")
    