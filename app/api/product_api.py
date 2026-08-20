from app.services.product_service import create_new_product, update_seller_product_attributes, delete_product_in_database, find_seller_products, find_user_search_products, seller_find_product, create_product_order
from sqlmodel import Session
from fastapi import APIRouter, status, Depends, HTTPException
from app.database_models.product_model import CreateProduct, ReadProduct, UpdateProduct
from app.database_config.database_connection import get_session
from app.core.jwt_token import get_user_token
from app.core import exceptions
from sqlalchemy.exc import DatabaseError
from app.database_models.order_model import CreateOrder

router = APIRouter()

@router.post("/products", status_code=status.HTTP_201_CREATED, response_model=ReadProduct)
def new_product(product: CreateProduct, session: Session=Depends(get_session), token: dict=Depends(get_user_token)):
        return create_new_product(product, session, token)

@router.patch("/product/{product_id}", status_code=status.HTTP_200_OK)
def product_update(product_id: int, product: UpdateProduct, seller: dict=Depends(get_user_token), session: Session=Depends(get_session)):
    try:
        return update_seller_product_attributes(product_id, product, seller, session)
    
    except exceptions.ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    except exceptions.SellerProductNotFound:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Product not found!")

@router.delete("/product-delete", status_code=status.HTTP_200_OK)
def product_delete(product_id: int, seller: dict=Depends(get_user_token), session: Session=Depends(get_session)):
    try:
        return delete_product_in_database(product_id, seller['id'], session)
    except exceptions.ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")

@router.get("/seller-products", status_code=status.HTTP_200_OK)
def get_products(seller: dict = Depends(get_user_token), session: Session=Depends(get_session)):
    try:
        return find_seller_products(seller['id'], session)
    except exceptions.ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found!")


@router.get("/search-product", status_code=status.HTTP_200_OK, response_model=list[ReadProduct])
def search_product(search: str, session: Session=Depends(get_session)):
    try:
        return find_user_search_products(search, session)

    except exceptions.ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found!")

@router.get("/seller_product", status_code=status.HTTP_200_OK)
def get_seller_product(product_id: int, seller: dict = Depends(get_user_token), session: Session = Depends(get_session)):
    try:
        return seller_find_product(product_id, seller['id'], session)

    except exceptions.ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found!")

@router.post("/buy-now/{product_id}", status_code=status.HTTP_201_CREATED)
def buy_now(product_id: int, create_order: CreateOrder, user: dict=Depends(get_user_token), session: Session=Depends(get_session)):
    try:
        return create_product_order(product_id, create_order, user['id'], session)
    except exceptions.UserNotFound:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User!")
    
    except exceptions.ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
    
    except exceptions.StockFinished:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product is out of stock!")
    
    except exceptions.QuantityOrderError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You are product quantity too high")
    
    except exceptions.InvalidQuantity:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid Quantity!")

