from app.services.admin_service import create_admin_account, CreateAdmin, Session
from app.core import exceptions
from app.api.user_api import APIRouter, Depends, get_session, HTTPException
from fastapi import status
from app.database_models.admin_model import ReadAdmin, AdminLogin
from app.services.admin_service import admin_login_by_email_and_password
from sqlalchemy.exc import DatabaseError

router = APIRouter()

@router.post("/create-admin", status_code=status.HTTP_201_CREATED, response_model=ReadAdmin)
def new_admin_registered(admin: CreateAdmin, session: Session=Depends(get_session)):
    try:
        return create_admin_account(admin, session)
    except exceptions.AdminAlreadyExist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Admin Account already exist at your email")

    except exceptions.DuplicateAdminData:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone number or email already exists!")

    except DatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error!")

@router.post("/admin-login", status_code=status.HTTP_200_OK)
def admin_login(admin: AdminLogin, session: Session = Depends(get_session)):
    try:
        return admin_login_by_email_and_password(admin, session)

    except exceptions.InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")

    except DatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error!")