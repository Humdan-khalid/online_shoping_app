from jose import jwt, JWTError , ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
import logging
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import secret_key, algorithm

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)


def verify_secret_keys():
    if not secret_key :
        raise ValueError("Secret Key not Found!")
    
    if not algorithm:
        raise ValueError("Algorithm not FOund!")

## this function create a token.
def create_token(user_data: dict, time_expiry: timedelta = timedelta(minutes=30)):
    verify_secret_keys()
    payload = user_data.copy()
    payload["exp"] = datetime.now(timezone.utc) + time_expiry
    payload['sub'] = str(user_data['id'])
    payload["type"] = "access"
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

## this function decode the token.
def verify_token(token: str):
    try:
        check_token = jwt.decode(token, secret_key, algorithms=[algorithm])
        return check_token
    except ExpiredSignatureError:
        logger.warning("Token has expired!")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired!")
    except JWTError:
        logger.warning("Invalid token!")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        

security = HTTPBearer()

def get_user_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return verify_token(token)