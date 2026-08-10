from sqlmodel import Session, select
from app.database_models.product_model import CreateProduct, Products, UpdateProduct
from app.database_models.cart_model import Cart
from app.core import exceptions
from app.repository.product_repo import product_save_in_database, find_product_in_database, find_seller_products_in_database, get_products, find_seller_product_with_id, find_product_with_id
from sqlalchemy.exc import DatabaseError
from app.core.log_config import logging
from app.repository.seller_repo import find_seller_in_database, get_seller_from_token
from app.repository.user_repo import get_user_by_id
from app.database_models.order_model import Orders, CreateOrder

def create_new_product(product: CreateProduct, session: Session, token: dict):
    try:
        seller = get_seller_from_token(token, session)

        if not seller:
            logging.warning(f"Unauthorized seller tried for the login, but system rejected the token.")
            raise exceptions.InvalidToken("Invalid seller token.")

        new_product = Products(
            name=product.name,
            price=product.price,
            weight=product.weight,
            colour=product.colour,
            brand=product.brand,
            description=product.description,
            quantity=product.quantity,
            seller_id=seller.id
        )

        product_save_in_database(new_product, session)
        return new_product

    except DatabaseError:
        logging.exception("Database error while created the new product.")
        raise

def update_product_attributes(product_id: int,  product_update: UpdateProduct, seller: dict, session: Session):
    try:
        db_seller = get_seller_from_token(seller, session)

        if not db_seller:
            logging.warning(f"Unauthorized seller tried to update the product, but system rejected the token. | seller_id: {seller['id']} | seller_email: {seller['email']}.")
            raise exceptions.UnauthorizedSeller("Unauthorized seller tried to update the product, but system rejected the token.")
        
        product = find_product_in_database(product_id, seller['id'], session)

        if not product or product.status == "Not Available":
            logging.warning(f"Seller found the product but product not found! | Product_id: {product_id}")
            raise exceptions.ProductNotFound("Product not found!")

        product_convert_dict = product_update.dict(exclude_none= True)
        print(product_update.dict(exclude_none=True))
        print(product_update.dict())

        for key, value in product_convert_dict.items():
            setattr(product, key, value)

        print(product_update)

        session.add(product)
        session.commit()

        return{"Message" : "Product successfully updated"}

    except DatabaseError:
        logging.exception("Database error while update the product data.")
        raise 


def delete_product_in_database(product_id: int, seller: int, session: Session):
    try:
        db_seller = find_seller_in_database(seller, session)

        if not db_seller:
            logging.warning(f"Unauthorized seller tried to delete the product, but system rejected the fake token. | seller_id: {seller} | product_id: {product_id}")
            raise exceptions.SellerNotExist("Unauthorized seller tried to delete the product, but system rejected the fake token. | seller_id: {seller}")

        db_product = find_product_in_database(product_id, seller, session)

        if not db_product:
            logging.warning(f"Seller find the product for deleting but product not found | product_id: {product_id} | seller_id: {seller}")
            raise exceptions.ProductNotFound("Product not found!")

        db_cart = session.exec(
            select(Cart).where(
                Cart.product_id == product_id
            )
        ).all()

        for cart in db_cart:
            session.delete(cart)

        db_product.status = "Not Available"

        session.add(db_product)
        session.commit()

        logging.info("Product successfully deleted to the Cart and successfully status change in database.")
        return{"message": "Successfully product status UnAvailable."}

    except DatabaseError:
        logging.exception("Database Error! While seller was tring to delete the product.")
        raise 


def find_seller_products(seller_id: int, session: Session):
    try:
        db_seller = find_seller_in_database(seller_id, session)

        if not db_seller:
            logging.warning(f"Unauthorized seller tried to get the products, but system rejected the fake token. | seller_id: {seller_id}")
            raise exceptions.SellerNotExist("Unauthorized seller tried to delete the product, but system rejected the fake token. | seller_id: {seller}")

        db_products = find_seller_products_in_database(seller_id, session)

        if not db_products:
            logging.warning(f"Seller did not find the products | Seller: {seller_id}")
            raise exceptions.ProductNotFound("Product not found!")

        return{
            "products": db_products
        }

    except DatabaseError:
        logging.exception("Database Error! While seller was fetching the products to the database.")
        raise exceptions.DatabaseError("Database Error!")

def find_user_search_products(search: str, session: Session):
    try:
        products = get_products(search, session)

        if not products:
            logging.warning("Products not found While user searched the products.")
            raise exceptions.ProductNotFound("Products not found!")

        return products

    except DatabaseError:
        logging.exception("Database Error! While user search the products.")
        raise

def seller_find_product(product_id:int , seller_id: int, session: Session):
    seller = find_seller_in_database(seller_id, session)

    if not seller:
        logging.warning("Unauthorized seller tried to find the product but system rejected the fake token!")
        raise exceptions.SellerNotExist("Unauthorized seller tried to find the product!")

    product = find_seller_product_with_id(product_id, seller_id, session)

    if not product:
        logging.warning(f"Seller try to find the product but Product not found | product_id:{product_id}")
        raise exceptions.ProductNotFound("Product not found")

    return product


def create_product_order(product_id: int, create_order: CreateOrder,  user: int, session: Session):
    try:
        db_user = get_user_by_id(user, session)

        if not db_user:
            logging.warning(f"Unauthorized user tried to create the order with fake token. | user_id: {user}")
            raise exceptions.UserNotFound("User not found")

        db_product = find_product_with_id(product_id, session)

        if not db_product:
            logging.warning(f"User give the invalid product id! | product_id: {product_id} | user: {user}")
            raise exceptions.ProductNotFound("Product not found!")

        if db_product.quantity <= 0:
            logging.warning(f"User give the invalid product quantity! | product_id: {product_id} | user: {user} | quantity: {create_order.quantity}")
            raise exceptions.StockFinished("Product is Out of stock!")

        
        if create_order.quantity > db_product.quantity:
            logging.warning(f"User give the product quantity very high to the available stock | product_id: {product_id} | user: {user} | quantity: {create_order.quantity} | Available stock: {db_product.quantity}")
            raise exceptions.QuantityOrderError("Quantity Error!")

        if create_order.quantity <= 0:
            logging.warning(f"User give the invalid product quantity {create_order.quantity}. | user_id: {db_user.id} | product_id: {db_product.id}")
            raise exceptions.InvalidQuantity("Invalid quantity")

        amount = db_product.price * create_order.quantity

        order = Orders(
            product_id=db_product.id,
            product_name=db_product.name,
            seller_id=db_product.seller_id,
            user_id=db_user.id,
            quantity=create_order.quantity,
            product_price=db_product.price,
            total_amount=amount,
            status=create_order.status
        )

        db_product.quantity -= order.quantity

        session.add(order)
        session.commit()
        session.refresh(order)

        logging.info(f"User successfully order created. | user_id: {db_user.id} | product_id: {db_product.id}.")
        return{"message": "Order submit successfully"}

    except DatabaseError:
        logging.exception(f"Database Error! While user created the order. | user_id: {db_user.id} | product_id: {db_product.id}")
        raise
    

    

    