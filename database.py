from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    age: str = Field(nullable=False)
    phone_number: str = Field(max_length=11 ,nullable=False)
    city: str = Field(nullable=False)
    email:  EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)

class CreateUser(SQLModel):
    name: str
    age: str
    phone_number: str
    city: str
    email: EmailStr
    password: str

