from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("database-url not found!")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    future=True
)

def create_tables():
    SQLModel.metadata.create_all(engine)

create_tables()
