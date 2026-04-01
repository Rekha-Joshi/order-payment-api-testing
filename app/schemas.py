#Schemas define the structure and validation rules for API request and response data.
#It defines what API expects and ensures that only valid data is accepted.

from pydantic import BaseModel, EmailStr
from typing import List

class CustomerCreate(BaseModel): #creating a class and it's inherting from BaseModel to validate + parse
    name: str
    email: EmailStr

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
