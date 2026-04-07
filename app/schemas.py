#Schemas define the structure and validation rules for API request and response data.
#It defines what API expects and ensures that only valid data is accepted.
from pydantic import BaseModel, EmailStr, Field
from typing import List

class CustomerCreate(BaseModel): #creating a class and it's inherting from BaseModel to validate + parse
    name: str = Field(..., min_length=1)
    email: EmailStr

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1) # ... mark this filed as required
    price: float = Field(..., gt=0) #gt grater than
    stock: int = Field(..., ge=0) #ge greater than & equal

class OrderItemCreate(BaseModel):
    product_id: int 
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    customer_id: int = Field(..., gt=0)
    items: List[OrderItemCreate] = Field(..., min_length=1)

class PaymentCreate(BaseModel):
    order_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
