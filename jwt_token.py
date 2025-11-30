from jose import jwt, JWTError , ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Header
import os


load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

if not SECRET_KEY or not ALGORITHM:
    raise ValueError("Secret Key or Algorithm not found!")

## this function create a token.
def create_token(user_data: dict, time_expiry: timedelta = timedelta(minutes=30)):
    payload = user_data.copy()
    payload["exp"] = datetime.now(timezone.utc) + time_expiry
    payload["sub"] = str(user_data["id"])
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

## this function decode the token.
def verify_token(token: str):
    try:
        check_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return check_token
    except JWTError:
        raise ValueError("Invalid Token")
    except ExpiredSignatureError:
        raise ValueError("token has expired!")

## this function verify the token type.
def user_token_verification(authorization: str = Header(...)):
    scheme, token = authorization.split()

    if scheme.lower() != "bearer":
        raise ValueError("Invalid Auth scheme")
    
    payload = verify_token(token)
    return payload

def create_refresh_token(user_data: dict, time_expiry: timedelta = timedelta(days=7)):
    payload = user_data.copy()
    payload["exp"] = datetime.now(timezone.utc) + time_expiry
    payload["sub"] = user_data["id"]
    payload["type"] = "refresh"
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_refresh_token(token: str):
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    try:
        if decoded.get("type") != "refresh":
            raise ValueError("Invalid token type (not refresh token)")
        return decoded
    
    except ExpiredSignatureError:
        raise ValueError("Refresh token expired")
    except JWTError:
        raise ValueError("Invalid refresh token.")
    
def create_access_token_with_refresh_token(refresh_token: str):
    decoded = verify_refresh_token(refresh_token)
    user_id = decoded["sub"]
    user_data = {"id": user_id}
    new_access_token = create_token(user_data)

    return{
        "access_token": new_access_token,
        "refresh_token": refresh_token
    }