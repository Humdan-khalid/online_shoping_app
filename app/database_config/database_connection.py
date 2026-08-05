from sqlmodel import SQLModel, create_engine, Session
from app.core.log_config import logger
from app.core.config import database_url


if not database_url:
    logger.critical("Database url not Found!")
    raise ValueError("Database url Not Found!")

engine = create_engine(
    database_url,
    echo=False,
    pool_size=10,
    max_overflow=20,
    future=True
)

def get_session():
    with Session(engine) as session:
        yield session
