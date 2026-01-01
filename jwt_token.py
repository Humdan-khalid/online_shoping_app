from jose import jwt, JWTError , ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Header, HTTPException, status
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

if not SECRET_KEY or not ALGORITHM:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Secret Key or Algorithm not found!")

## this function create a token.
def create_token(user_data: dict, time_expiry: timedelta = timedelta(minutes=30)):
    payload = user_data.copy()
    payload["exp"] = datetime.now(timezone.utc) + time_expiry
    payload["sub"] = str(user_data["id"])
    payload["type"] = "access"
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

## this function decode the token.
def verify_token(token: str):
    try:
        check_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return check_token
    except ExpiredSignatureError:
        logger.warning("Token expired!")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired!")
    except JWTError:
        logger.warning("Invalid token!")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token")
        

## this function verify the token type.
def user_token_verification(token: str = Header(...)):
    parts = token.split()

    if len(parts) != 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Authorization header format. Use: Bearer <token>")
    
    scheme, token = parts

    if scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Invalid Auth scheme, expected Bearer")
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
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if decoded.get("type") != "refresh":
            raise ValueError("Invalid token type (not refresh token)")
        return decoded
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired!")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token.")
    
def create_access_token_with_refresh_token(refresh_token: str):
    decoded = verify_refresh_token(refresh_token)
    user_id = decoded["sub"]
    user_data = {"id": user_id}
    new_access_token = create_token(user_data)

    return{
        "access_token": new_access_token,
        "refresh_token": refresh_token
    }

