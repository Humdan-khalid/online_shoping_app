from app.database_models.admin_model import Admin, CreateAdmin, AdminLogin
from sqlmodel import Session, select

def get_admin_in_database_by_email(email: str, session: Session):
    db_admin = session.exec(select(Admin).
                           where(Admin.email == email)).first()

    return db_admin

def admin_data_save_in_database(admin: CreateAdmin,session: Session):
    session.add(admin)
    session.commit()
    session.refresh(admin)

def find_admin_by_email(email: str, session: Session):
    db_admin = session.exec(
        select(Admin).where
            (Admin.email == email
        )
    ).first()

    return db_admin