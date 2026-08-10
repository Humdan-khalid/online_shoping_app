from passlib.context import CryptContext
from app.core.log_config import logger


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=10
)

def create_hash_password(password: str):
    if password is None:
        logger.error("Password not found!")
        raise ValueError("Password not found!")
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(plain_password: str, hash_password: str):
        return pwd_context.verify(plain_password, hash_password)