from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Products(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    price: float = Field(nullable=False)
    weight: str = Field(nullable=False)
    colour: str = Field(nullable=True)
    brand: str = Field(nullable=False)
    description: str = Field(nullable=True)
    quantity: int = Field(nullable=False,)
    seller_id: int = Field(foreign_key="sellers.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="Available")

class CreateProduct(BaseModel):
    name: str = Field(min_length=3, regex=r"^[a-bA-B]")
    price: float = Field(ge=1)
    weight: str
    colour: str
    brand: str
    description: str
    quantity: int

class UpdateProduct(BaseModel):
    name: Optional[str] = None 
    price: Optional[float] = None
    weight: Optional[str] = None
    colour: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None

class ReadProduct(BaseModel):
    name: str 
    price: float
    weight: str
    colour: str
    brand: str
    description: str
    quantity: int