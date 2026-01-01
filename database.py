from sqlmodel import SQLModel, Field, Column
from pydantic import EmailStr, BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String

class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, min_length=3, max_length=25)
    age: int = Field(nullable=False, max_length=2)
    phone_number: str = Field(nullable=False, max_length=11)
    city: str = Field(nullable=False)
    create_at: datetime = Field(default_factory=datetime.utcnow)
    email:  EmailStr = Field(index=True, unique=True, min_length=13, max_length=30, nullable=False)
    password: str = Field(nullable=False, min_length=8)

class CreateUser(BaseModel):
    name: str = Field(min_length=3, max_length=25)
    age: int = Field(ge=12, le=100)
    phone_number: str = Field(max_length=11)
    city: str
    email: EmailStr = Field(min_length=13, max_length=30)
    password: str = Field(min_length=8)

class VerifyUser(BaseModel):
    email: EmailStr
    password: str

class Admin(SQLModel, table=True):
    id: int = Field(default= None, primary_key=True)
    name: str = Field(nullable=False, min_length=3, max_length=25)
    age: int = Field(nullable=False, ge=20 , le=80)
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False, min_length=8)
    created_at: datetime = Field(default_factory= datetime.utcnow)

class CreateAdmin(BaseModel):
    name: str = Field(min_length=3, max_length=25)
    age: int = Field(ge=20 , le=80)
    email: EmailStr
    password: str = Field(min_length=8)
    
class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class Sellers(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=25, nullable=False)
    age: int = Field(nullable=False, ge=18, le=100)
    phone_number: str = Field(nullable=False, max_length=11)
    city: str = Field(nullable=False)
    account_type: str = Field(nullable=False, default="Seller")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False, min_length=8)

class CreateSeller(BaseModel):
    name: str = Field(min_length=3, max_length=25)
    age: int = Field(ge=18, le=100)
    phone_number: str = Field(max_length=11)
    city: str
    email: EmailStr
    password: str = Field(min_length=8)

class VerifySeller(BaseModel):
    email: EmailStr
    password: str


class Products(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, min_length=3, max_length=30)
    price: float = Field(nullable=False, gt=0)
    size: str = Field(nullable=False)
    colour: str = Field(nullable=True)
    brand: str = Field(nullable=False)
    description: str = Field(nullable=True, max_length=80)
    quantity: int = Field(nullable=False, gt=0)
    seller_id: int = Field(foreign_key="sellers.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CreateProduct(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    price: float = Field(gt=0)
    size: Optional[str] = None
    colour: Optional[str] = None
    brand: str
    description: Optional[str] = Field(max_length=80)
    quantity: int = Field(gt=0)

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    size: Optional[str] = None
    colour: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    size: Optional[str]= None
    colour: Optional[str]=None
    brand: str
    description: Optional[str] = None
    price: float

    class Config:
        orm_mode = True

class Orders(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    product_id: int = Field(foreign_key="products.id")
    seller_id: int = Field(foreign_key="sellers.id")
    user_id: int = Field(foreign_key="users.id")
    quantity: int = Field(nullable=False, gt=0)
    price: float = Field(nullable=False, ge=0)
    paid: float = Field(nullable=False, ge=0)
    status: str = Field(nullable=False)

class CreateOrder(BaseModel):
    quantity: int

class ShowProducts(BaseModel):
    name: str
    status: str
    quantity: int
    paid: float
    price: float

    class Config:
        orm_mode = True

class Cart(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    product_name: str = Field(nullable=False)
    product_id : int = Field(foreign_key="products.id")
    customer_id: int = Field(foreign_key="users.id")
    seller_id: int = Field(foreign_key="sellers.id")
    status: str = Field(nullable=False)

class CartResponse(BaseModel):
    product_name: str
    customer_name: str
    status: str