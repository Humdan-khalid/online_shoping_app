from app.database_models.admin_model import Admin, CreateAdmin, AdminLogin
from sqlmodel import Session, select

def get_admin_in_database_by_email(admin: CreateAdmin, session: Session):
    db_admin = session.exec(select(Admin).
                           where(Admin.email == admin.email)).first()

    return db_admin

def admin_data_save_in_database(admin: CreateAdmin,session: Session):
    session.add(admin)
    session.commit()
    session.re

def admin_login_by_email(admin: AdminLogin, session: Session):
    db_admin = session.exec(
        select(Admin).where
            (Admin.email == admin.email
        )
    ).first()

    return db_admin