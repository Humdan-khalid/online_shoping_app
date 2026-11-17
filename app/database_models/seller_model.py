from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import EmailStr, BaseModel, Field as PydanticField

class Sellers(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    age: int = Field(nullable=False)
    phone_number: str = Field(nullable=False, unique=True)
    city: str = Field(nullable=False)
    account_type: str = Field(nullable=False, default="Seller")
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CreateSeller(BaseModel):
    name: str = PydanticField(min_length=3, pattern=r"^[a-zA-Z]+(?: [a-zA-Z]+)*$")
    age: int = PydanticField(ge=18, le=100)
    phone_number: str = PydanticField(pattern=r"^03[0-9]{9}$")
    city: str = PydanticField(min_length=4, pattern=r"^[a-zA-Z]+(?: [a-zA-Z]+)*$")
    email: EmailStr
    password: str = PydanticField(min_length=8, max_length=35)

class ReadSeller(BaseModel):
    id: int
    name: str
    age: int
    phone_number: str
    account_type: str
    city: str
    email: EmailStr


class SellerLogin(BaseModel):
    email: EmailStr = Field(regex=r"^[a-b0-9]+@gmail\.com$")
    password: str
    