from fastapi import FastAPI

from app.schemas import CustomerCreate
from app.schemas import ProductCreate
from app.schemas import OrderCreate

app = FastAPI()

@app.get("/")
def read_root():
    return{"message": "Order Payment API is running."}

@app.post("/customers", status_code=201)
def create_customer(customer: CustomerCreate):
    return {
        "message":"Customer Created",
        "data": customer
    }

@app.get("/customers/{customer_id}")
def get_customer(customer_id:int):
    return {
        "customer_id": customer_id,
        "name": "Sample user",
        "email": "sample@test.com"
    }

@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    return {
        "message": "Product Created",
        "data": product
    }
@app.get("/products/{product_id}")
def get_product(product_id:int):
    return {
        "product_id": product_id,
        "name": "XYZ",
        "price": 2.345,
        "stock": 50
    }
@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    return {
        "message": "Order Created",
        "data": order
    }
@app.get("/orders/{order-id}")
def get_order(order_id: int):
    return {
        "order_id": order_id,
        "customer_id": 1,
        "status": "PENDING",
        "total_amount": 250.0,
        "items": [
            {
                "product_id": 1,
                "quantity": 2,
                "price": 100.0,
                "subtotal": 200.0
            },
            {
                "product_id": 2,
                "quantity": 1,
                "price": 50.0,
                "subtotal": 50.0
            }
        ]
    }