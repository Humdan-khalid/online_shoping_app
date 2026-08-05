from fastapi import APIRouter, status, Depends,HTTPException
from app.database_models.seller_model import CreateSeller, ReadSeller, SellerLogin
from sqlmodel import Session
from app.database_config.database_connection import get_session
from app.services.seller_service import create_new_seller_account, seller_account_login
from app.core import exceptions
from sqlalchemy.exc import DatabaseError

router = APIRouter()

@router.post("/seller-account", status_code=status.HTTP_201_CREATED, response_model=ReadSeller)
def seller_account(seller: CreateSeller, session: Session = Depends(get_session)):
    try:
        return create_new_seller_account(seller, session)

    except exceptions.SellerAlreadyExist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Seller already exist at email!")

    except DatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error!")


@router.post("/seller-login", status_code=status.HTTP_200_OK)
def seller_login(seller: SellerLogin, session: Session=Depends(get_session)):
    try:
        return seller_account_login(seller, session)

    except exceptions.SellerNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password!")

    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error!") 