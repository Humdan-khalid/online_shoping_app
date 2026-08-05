from sqlmodel import SQLModel, Field
from pydantic import BaseModel

## I will add created_at column 
class Orders(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    product_name: str = Field(nullable=False)
    product_id: int = Field(foreign_key="products.id")
    seller_id: int = Field(foreign_key="sellers.id")
    user_id: int = Field(foreign_key="users.id")
    quantity: int = Field(nullable=False)
    product_price: float = Field(nullable=False)
    total_amount: float = Field(nullable=False)
    status: str = Field(nullable=False)

class CreateOrder(BaseModel):
    quantity: int = Field(ge=0)
    status: str = Field(default="Confirmed")
