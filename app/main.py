from fastapi import FastAPI
from app.api import user_api, admin_api, seller_api, product_api, cart_api


app = FastAPI()

app.include_router(admin_api.router)
app.include_router(user_api.router)
app.include_router(seller_api.router)
app.include_router(product_api.router)
app.include_router(cart_api.router)


# from fastapi import FastAPI, HTTPException, status, Depends
# from database_models import Users , CreateUser, VerifyUser, CreateSeller, Sellers, VerifySeller, Products, CreateProduct, UpdateProduct, ProductResponse, Orders, CreateOrder, ShowProducts, Cart, CartResponse, Admin, CreateAdmin, AdminLogin
# from sqlmodel import SQLModel, Session, select
# from app.database_config.database_connection import engine
# from password_hash import create_hash_password, check_verify_password
# from jwt_token import create_token, user_token_verification
# import logging

# def get_session():
#     with Session(engine) as session:
#         yield session

# app = FastAPI()

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# @app.post("/users", status_code=status.HTTP_201_CREATED)
# def create_new_user(user: CreateUser, session: Session = Depends(get_session)):
#     if session.exec(select(Users).where(Users.email == user.email)).first():
#         logger.warning(f"Already user acount exist!")
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already exist!")

#     data = Users(
#         name = user.name.capitalize(),
#         age = user.age,
#         phone_number = user.phone_number,
#         city = user.city.capitalize(),
#         email = user.email,
#         password = create_hash_password(user.password)
#     )
#     session.add(data)
#     session.commit()
#     session.refresh(data)

#     logger.info(f"New user created | id={data.id}")

#     return{"id": data.id,
#            "name": data.name,
#            "email": data.email}

# @app.post("/login/users", status_code=status.HTTP_200_OK)
# def user_login(user: VerifyUser, session: Session = Depends(get_session)):
#     db_user = session.exec(select(Users).where(Users.email == user.email)).first()
#     if not db_user:
#         logger.warning(f"user wrong login attempt! with wrong email")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password!")


#     if not check_verify_password(user.password , db_user.password):
#         logger.warning(f"user wrong login attempt! with wrong password.")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")

#     payload: dict = {
#         "id": db_user.id,
#         "email": db_user.email
#     }

#     token = create_token(payload)
#     logger.info(f"user successfully login | id: {db_user.id}")

#     return{"access_token": token,
#            "token_type": "Bearer"}


# @app.post("/logout")
# def logout():
#     return{"message": "logout"}

# @app.post("/sellers", status_code=status.HTTP_201_CREATED)
# def create_seller_account(seller: CreateSeller, session: Session = Depends(get_session)):
#     if session.exec(select(Sellers).where(Sellers.email == seller.email)).first():
#         logger.warning(f"account already exist at this email.")
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already exist!")

#     new_seller = Sellers(
#         name = seller.name.capitalize(),
#         age = seller.age,
#         phone_number = seller.phone_number,
#         city = seller.city.capitalize(),
#         email = seller.email.lower(),
#         password = create_hash_password(seller.password)
#     )

#     session.add(new_seller)
#     session.commit()
#     session.refresh(new_seller)

#     logger.info(f"new seller created | seller_id: {new_seller.id}")

#     return{"id": new_seller.id,
#            "name": new_seller.name,
#            "email": new_seller.email}

# @app.post("/login", status_code=status.HTTP_200_OK)
# def seller_login(seller: VerifySeller, session: Session = Depends(get_session)):
#     db_seller = session.exec(select(Sellers).where(Sellers.email == seller.email)).first()

#     if not db_seller:
#         logger.warning(f"seller wrong login attempt! with wrong email")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")
    
#     if not check_verify_password(seller.password, db_seller.password):
#         logger.warning(f"seller wrong login attempt! with wrong password")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")

#     payload = {
#         "id": db_seller.id,
#         "email": db_seller.email
#     }

#     token = create_token(payload)

#     logger.info(f"seller successfully login | seller_id: {db_seller.id}.")

#     return{"access_token": token,
#            "token_type": "Bearer"}

# @app.post("/products", status_code=status.HTTP_201_CREATED)
# def create_product(product: CreateProduct, session: Session = Depends(get_session), seller: dict = Depends(user_token_verification)):
#     db_seller = session.exec(select(Sellers).where(Sellers.email == seller["email"])).first()

#     if not db_seller:
#         logger.warning("Invalid seller for create the product.")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unathorized Seller!")

#     new_product = Products(
#         name=product.name.capitalize(),
#         price=product.price,
#         size=product.size.capitalize() if product.size else None,
#         colour=product.colour.capitalize() if product.colour else None,
#         brand=product.brand.capitalize(),
#         description=product.description.capitalize() if product.description else None,
#         quantity=product.quantity,
#         seller_id=seller["id"]
#     )

#     session.add(new_product)
#     session.commit()
#     session.refresh(new_product)

#     logger.info(f"new product created | seller_id: {new_product.seller_id} | product_id: {new_product.id}.")

#     statement = (
#             select(
#                 Sellers   .name.label("seller_name"),
#                 Products.name.label("product_name"),
#                 Products.id.label("product_id")
#             )    
#                 .join(Products, Products.seller_id == Sellers.id)
#                 .where(Products.id == new_product.id)
#                 )
#     result = session.exec(statement).mappings().first()

#     return result

# @app.patch("/products/{product_id}" ,status_code=status.HTTP_200_OK)
# def update_product_data(product_id: int, product: UpdateProduct, session: Session = Depends(get_session), seller: dict = Depends(user_token_verification)):
#     db_seller = session.exec(select(Sellers).where(Sellers.id == seller["id"])).first()
#     db_product = session.exec(select(Products).where(Products.seller_id == seller["id"], Products.id == product_id)).first()

#     if not db_seller:
#         logger.warning(f"Invalid seller | seller_id: {seller['id']}")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized seller!")
    
#     if not db_product:
#         logger.warning(f"product not found | product_id: {product_id}.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found!")
    
#     product_update = product.dict(exclude_none=True)

#     for key, value in product_update.items():
#         setattr(db_product, key, value)

#     session.add(db_product)
#     session.commit()

#     statement=(
#         select(
#             Products.id.label("product_id"),
#             Products.name.label("product_name"),
#             Sellers.name.label("seller_name")
#         )
#         .join(Products, Products.seller_id == Sellers.id)
#         .where(Products.id == product_id)
#     )
#     result = session.exec(statement).mappings().first()

#     logger.info(f"product {product_update} successfully update to seller_id: {db_product.seller_id}.")
#     return result
        
# @app.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
# def delete_product(product_id: int, session: Session = Depends(get_session), seller: dict = Depends(user_token_verification)):
#     db_product = session.exec(select(Products).where(Products.seller_id == seller["id"], Products.id == product_id)).first()

#     if not db_product:
#         logger.warning(f"product_id not found! | seller_id: {seller['id']} | product_id: {product_id}.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found!")
    
#     db_cart = session.exec(select(Cart).where(Cart.product_id == product_id)).all()

#     for items in db_cart:
#         session.delete(items)

#     db_orders = session.exec(select(Orders).where(Orders.product_id == product_id)).all()

#     for products in db_orders:
#         session.delete(products)

#     session.delete(db_product)
#     session.commit()

#     logger.info(f"seller successfully deleted the product | product_id: {db_product.id} | seller_id: {db_product.seller_id}.")
#     return{"message": "product deleted successfully"}

# @app.get("/profile", status_code=status.HTTP_200_OK)
# def get_products(session: Session = Depends(get_session), seller: dict = Depends(user_token_verification)):
#     db_product = session.exec(select(Products).where(Products.seller_id == seller["id"])).all()

#     if not db_product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found!")
    
#     logger.info("seller check the products")
#     return{"products": db_product}

# @app.get("/profile/{product_id}", status_code=status.HTTP_200_OK)
# def seller_get_single_product(product_id: int, session: Session = Depends(get_session), seller: dict = Depends(user_token_verification)):
#     db_product = session.exec(select(Products).where(Products.seller_id == seller["id"], Products.id == product_id)).first()

#     if not db_product:
#         logger.warning(f"product not found! | seller_id: {seller['id']} | product_id: {product_id}.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found!")
    
#     logger.info(f"seller sucessfully check the product | product_id: {product_id}.")
#     return{"Product": db_product}

# @app.get("/products", response_model= list[ProductResponse], status_code=status.HTTP_200_OK)
# def get_user_products(session: Session = Depends(get_session)):
#     db_products = session.exec(select(Products)).all()
#     return db_products


# @app.get("/products/{search}", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
# def user_search_products(search: str, session: Session = Depends(get_session)):
#     db_products = session.exec(select(Products).where(Products.name.ilike(f"%{search}%"))).all()

#     if not db_products:
#         logger.warning(f"product not found | customer search {search}.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found!")
    
#     logger.info(f"Customer successfully search the product | customer search {search}")
#     return db_products

# @app.post("/carts/{product_id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
# def cart(product_id: int, session: Session = Depends(get_session), user: dict = Depends(user_token_verification)):
#     db_user = session.exec(select(Users).where(Users.id == user["id"])).first()

#     if not db_user:
#         logger.warning("Invalid user!")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="please create user account!")
    
#     db_product = session.exec(select(Products).where(Products.id == product_id)).first()
#     if not db_product:
#         logger.warning(f"product not found | product_id: {product_id} | user_id: {user['id']}")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
    
#     cart = Cart(
#         product_name=db_product.name,
#         product_id=db_product.id,
#         customer_id=user["id"],
#         seller_id=db_product.seller_id,
#         status="Pending"
#     )

#     session.add(cart)
#     session.commit()
#     session.refresh(cart)
    
#     statement = (
#             select(
#                 Users.name.label("customer_name"),
#                 Products.name.label("product_name"),
#                 Cart.status
#                 )

#             .join(Cart, Cart.customer_id == Users.id)
#             .join(Products, Products.id == Cart.product_id)
#             .where(Cart.id == cart.id)
#             )
    
#     result = session.exec(statement).first()
            


#     logger.warning(f"customer cart successfully created | customer_id: {cart.customer_id} | product_id: {cart.product_id}.")
#     return result
    

# @app.post("/orders/{product_id}", status_code=status.HTTP_201_CREATED)
# def create_order(order: CreateOrder, product_id: int, session: Session = Depends(get_session), user: dict = Depends(user_token_verification)):
#     if not session.exec(select(Users).where(Users.id == user["id"])).first():
#         logger.warning(f"Invalid user | user_id: {user['id']}")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user!")
    
#     db_product = session.exec(select(Products).where(Products.id == product_id)).first()
#     db_cart=session.exec(select(Cart).where(Cart.customer_id == user["id"], Cart.product_id == product_id)).first()
    
#     if not db_product:
#         logger.warning(f"Product not found! | {product_id}.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found!")
    
#     if not db_cart:
#         logger.warning("Customer did not add to cart.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found!")
    
#     if db_product.quantity <= 0:
#         logger.warning(f"Product is out of stock | product_id: {product_id}.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product is out of stock.")

    
#     total_price = db_product.price * order.quantity

#     order_obj = Orders(
#         name=db_product.name,
#         product_id=db_product.id,
#         seller_id=db_product.seller_id,
#         user_id=user["id"],
#         quantity=order.quantity,
#         price=db_product.price,
#         paid=total_price,
#         status="Confirmed"
#     )

#     if order.quantity <= 0:
#         logger.warning("Invalid quantity.")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product is out of stock")

#     if db_product.quantity < order.quantity:
#         logger.warning("Customer order is too long from stock.")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"your order is too much.Total {db_product.quantity} availble at store.")
    
#     db_product.quantity -= order.quantity
    
#     session.add(order_obj)
#     session.add(db_product)
#     session.delete(db_cart)
#     session.commit()
#     session.refresh(order_obj)

#     logger.info("Order created successfully")

#     return{"id": order_obj.id,
#            "name": order_obj.name,
#            "price": order_obj.price}

# @app.get("/orders", status_code=status.HTTP_200_OK)
# def get_orders(session: Session = Depends(get_session), user: dict = Depends(user_token_verification)):
#     statement=(
#         select(
#             Users.name.label("user_name"),
#             Orders.name.label("product_name"),
#             Orders.seller_id.label("Seller_id"),
#             Orders.quantity.label("quantity"),
#             Orders.paid.label("paid")
#         )
        
#         .join(Orders, Users.id == Orders.user_id).where(Orders.user_id == user["id"])
#         )
    
#     result=session.exec(statement).mappings().all()

#     logger.info("user check the total orders.")

#     return result

# @app.post("/admins", status_code=status.HTTP_201_CREATED)
# def create_admin(admin_data: CreateAdmin, session: Session = Depends(get_session)):
#     db_admin = session.exec(select(Admin).where(Admin.email == admin_data.email)).first()

#     if db_admin:
#         logger.warning("account already exist at this email.")
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already account exist.")
    
#     new_admin = Admin(
#         name=admin_data.name,
#         age=admin_data.age,
#         email=admin_data.email,
#         password=create_hash_password(admin_data.password)
#     )

#     session.add(new_admin)
#     session.commit()
#     session.refresh(new_admin)
#     logger.info(f"admin account successfully created | id: {new_admin.id}." )

#     return{"message": "admin created successfully"}

# @app.post("/admin/login", status_code=status.HTTP_200_OK)
# def verify_admin(admin: AdminLogin, session: Session = Depends(get_session)):
#     db_admin = session.exec(select(Admin).where(Admin.email == admin.email)).first()

#     if not db_admin:
#         logger.warning("admin login attempt failed with wrong email.")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")
    
#     if not check_verify_password(admin.password , db_admin.password):
#         logger.warning("admin login attempt failed with wrong password.")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")
    
#     payload = {
#             "id": db_admin.id,
#             "email": db_admin.email
#     }

#     token = create_token(payload)
#     logger.warning(f"admin login successfully | admin_id: {db_admin.id}.")
#     return{"access_token": token,
#            "token_type": "bearer"}

# @app.delete("/delete_seller/{seller_id}", status_code=status.HTTP_200_OK)
# def delete_seller(seller_id: int, session: Session=Depends(get_session), admin: dict=Depends(user_token_verification)):
#     db_admin = session.exec(select(Admin).where(Admin.email == admin['email'])).first()
    
#     if not db_admin:
#         logger.warning(f"Unauthorized admin was deleted of the seller. | seller_id: {seller_id}.")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized admin.")
    
#     db_cart = session.exec(select(Cart).where(Cart.seller_id == seller_id)).all()

#     for cart in db_cart:
#         session.delete(cart)
#         logger.warning("Seller orders successfully deleted.")

#     db_order = session.exec(select(Orders).where(Orders.seller_id == seller_id)).all()
    
#     for order in db_order:
#         session.delete(order)

#     db_products = session.exec(select(Products).where(Products.seller_id == seller_id)).all()

#     for product in db_products:
#         session.delete(product)
#         logger.warning("Seller products successfully deleted.") 
    
#     db_seller = session.exec(select(Sellers).where(Sellers.id == seller_id)).first()
    
#     if not db_seller:
#         logger.warning(f"admin give the invalid seller_id | admin_id: {admin['id']} | seller_id: {seller_id}.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found!")

#     session.delete(db_seller)
#     session.commit()

    
#     return{"message": f"admin deleted the seller | seller_id: {seller_id} | admin_id: {admin['id']}."}

# @app.post("/users/{user_id}", status_code=status.HTTP_200_OK)
# def delete_user(user_id: int, session: Session=Depends(get_session), admin: dict=Depends(user_token_verification)):
#     db_admin = session.exec(select(Admin).where(Admin.id == admin["id"])).first()
    
#     if not db_admin:
#         logger.warning("Unauthorized admin!")
#     db_user = session.exec(select(Users).where(Users.id == user_id)).first()
    
#     if not db_user:
#         logger.warning(f"User not found! | admin_id: {admin['id']} | user_id: {user_id}")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    
#     db_cart = session.exec(select(Cart).where(Cart.customer_id == user_id)).all()

#     for cart in db_cart:
#         session.delete(cart)

#     db_orders = session.exec(select(Orders).where(Orders.user_id == user_id)).all()

#     for order in db_orders:
#         session.delete(order)

#     session.delete(db_user)
#     session.commit()
#     logger.info("admin delete the user successfully.")

#     return{"message": "User deleted Successfully"}

# @app.delete("/product{product_id}", status_code=status.HTTP_200_OK)
# def delete_product(product_id: int, session: Session=Depends(get_session), admin:dict=Depends(user_token_verification)):
#     db_admin = session.exec(select(Admin).where(Admin.id == admin["id"])).first()
    
#     if not db_admin:
#         logger.warning(f"Unauthorized admin found! | admin_id: {admin['id']}.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    
#     db_product = session.exec(select(Products).where(Products.id == product_id)).first()

#     if not db_product:
#         logger.warning(f"Product not found | admin_id: {admin['id']} | product_id: {product_id}.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
    
#     db_cart = session.exec(select(Cart).where(Cart.product_id == product_id)).all()

#     for cart in db_cart:
#         session.delete(cart)
    
#     db_orders = session.exec(select(Orders).where(Orders.product_id == product_id)).all()

#     for order in db_orders:
#         session.delete(order)

#     session.delete(db_product)
#     session.commit()

#     logger.info(f"admin deleted the product successfully | admin_id: {admin['id']} product_id: {db_product.id}.")
#     return{"message": "Product deleted successfully."}