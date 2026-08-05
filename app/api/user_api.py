from fastapi import status, Depends, HTTPException, APIRouter
from sqlmodel import Session
from app.database_config.database_connection import get_session
from app.database_models.user_model import CreateUser, ReadUser, LoginUser
from app.services.user_service import create_user_account, login_user_by_email
from app.core import exceptions
from sqlalchemy.exc import DatabaseError

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=ReadUser)
def create_user_new_account(user: CreateUser, session: Session = Depends(get_session)):
    try:
        return create_user_account(user, session)

    except exceptions.UserAlreadyExist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exist at your email")
    
    except DatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error!")
    
@router.post("/user-login", status_code=status.HTTP_200_OK)
def user_login(user: LoginUser, session: Session = Depends(get_session)):
    try:
        db_user = login_user_by_email(user, session)
        return db_user
    
    except exceptions.InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password!")
    
    except DatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error!")