from fastapi import FastAPI
from app.api import user_api, admin_api, seller_api, product_api, cart_api
from app.core import exceptions, handlers
from sqlalchemy.exc import DatabaseError

app = FastAPI()

app.include_router(admin_api.router)
app.include_router(user_api.router)
app.include_router(seller_api.router)
app.include_router(product_api.router)
app.include_router(cart_api.router)

app.add_exception_handler(exceptions.UnauthorizedSeller, handlers.unauthorized_seller_handler)
app.add_exception_handler(exceptions.TokenExpired, handlers.token_expired_handler)
app.add_exception_handler(DatabaseError, handlers.database_error_handler)
app.add_exception_handler(exceptions.ProductNotFound, handlers.product_not_found_error_handler)