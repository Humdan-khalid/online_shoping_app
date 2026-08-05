from app.database_models.user_model import Users
from sqlmodel import Session, select
from app.database_models.user_model import LoginUser, CreateUser

def get_user_by_email_in_database(user: CreateUser, session: Session):
        db_user = session.exec(
            select (Users).where(
                Users.email == user.email
            )
        ).first()

        return db_user
    
def get_logged_in_user_by_email(user: LoginUser, session: Session):
    db_user = session.exec(
          select(Users).where(
                Users.email == user.email
          )
    ).first()

    return db_user


def new_user_save_in_database(user: CreateUser, session: Session):
    session.add(user)
    session.commit()
    session.refresh(user)

def get_user_by_id(user_id: int, session: Session):
    db_user = session.exec(
         select(Users).where(
              Users.id == user_id
         )
    ).first()

    return db_user
