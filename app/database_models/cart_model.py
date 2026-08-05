from sqlmodel import SQLModel, Field
from pydantic import BaseModel

## I will add created_at column
class Cart(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    product_name: str = Field(nullable=False)
    product_id : int = Field(foreign_key="products.id")
    customer_id: int = Field(foreign_key="users.id")
    seller_id: int = Field(foreign_key="sellers.id")
    quantity: int = Field(nullable=False)
    status: str = Field(nullable=False, default="Pending")
