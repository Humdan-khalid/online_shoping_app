from fastapi.responses import JSONResponse

def unauthorized_seller_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail": "Unauthorized Seller!"}
    )

def token_expired_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail": "Seller token has expired!"}
    )

def database_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server error!"}
    )

def product_not_found_error_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Product not found!"}
    )

def token_invalid_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail":"Invalid token!"}
    )