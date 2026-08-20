from fastapi import FastAPI
from app.api import user_api, admin_api, seller_api, product_api, cart_api
from app.core import exceptions
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError

app = FastAPI()

app.include_router(admin_api.router)
app.include_router(user_api.router)
app.include_router(seller_api.router)
app.include_router(product_api.router)
app.include_router(cart_api.router)


@app.exception_handler(exceptions.Unauthorized)
def unauthorized_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)}
    )

@app.exception_handler(exceptions.TokenExpired)
def token_expired_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)}
    )

@app.exception_handler(DatabaseError)
def database_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error!"}
    )