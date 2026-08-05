from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr, Field as PydanticField
from datetime import datetime


class Users(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    age: int = Field(nullable=False)
    phone_number: str = Field(nullable=False)
    city: str = Field(nullable=False)
    email: EmailStr = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CreateUser(BaseModel):
    name: str = PydanticField(pattern=r"^[A-Za-z]+(?: [A-Za-z]+)*$")
    age: int = Field(ge=10, le=101)
    phone_number: str = PydanticField(pattern=r"^03[0-9]{9}$")
    city: str = PydanticField(pattern=r"^[a-zA-Z]+$")
    email: EmailStr = PydanticField(pattern=r"^[a-z][a-z0-9]+@gmail\.com$")
    password: str = Field(min_length=8 , max_length=25)


class ReadUser(BaseModel):
    name: str
    age: int
    phone_number: str
    city: str
    email: EmailStr

class LoginUser(BaseModel):
    email: EmailStr = Field(regex=r"^[a-z][a-z0-9]+@gmail\.com$")
    password: str
