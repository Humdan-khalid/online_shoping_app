from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
print(DATABASE_URL)

if not DATABASE_URL:
    raise ValueError("database-url not found")

ENGINE = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    future=True
)

