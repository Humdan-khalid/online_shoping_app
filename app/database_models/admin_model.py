from sqlmodel import SQLModel, Field
from pydantic import EmailStr, BaseModel
from datetime import datetime

class Admin(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    age: int = Field(nullable=False)
    city: str = Field(nullable=False)
    phone_number: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable = False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CreateAdmin(BaseModel):
    name: str = Field(min_length=3, max_length=40, regex=r"^[a-zA-Z]+$")
    age: int = Field(ge=21, le=101, regex=r"^(1[89]|[2-9][0-9]|100)$")
    city: str = Field(min_length=4, regex=r"^[a-zA-z]+$")
    phone_number: str = Field(min_length=11, max_length=11, regex=r"^03[0-9]{9}+$")
    email: EmailStr = Field(regex=r"^[a-z][a-z0-9]+@gmail\.com$")
    password: str = Field(min_length=12, max_length=30)


class AdminLogin(BaseModel):
    email: EmailStr = Field(regex=r"^[a-z][a-z0-9]+@gmail\.com")
    password: str


class ReadAdmin(BaseModel):
    name: str
    age: int
    city: str
    phone_number: str
    email: str