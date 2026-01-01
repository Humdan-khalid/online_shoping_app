from passlib.context import CryptContext
from fastapi import HTTPException, status
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=10
)

def create_hash_password(password: str):
    if password is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password is None!")
    hashed_password = pwd_context.hash(password)
    return hashed_password

def check_verify_password(plain_password: str, hash_password: str):
        try:
            verify_password = pwd_context.verify(plain_password, hash_password)
            return verify_password
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")
