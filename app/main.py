from fastapi import FastAPI

# Import request validation schemas (Pydantic models)
from app.schemas import CustomerCreate, ProductCreate, OrderCreate

# Import database engine and models
from app.database import engine, Base
from app import models

# Create FastAPI app instance
app = FastAPI()

# Base is the parent class for all ORM models
# metadata - it stores info about all tables created using Base
# creat_all - create tables that doens't exist already
# engine - tell which DB to connect to
Base.metadata.create_all(bind=engine)

# Root endpoint to verify API is running
@app.get("/")
def read_root():
    return {"message": "Order Payment API is running."}

# Create a new customer
# FastAPI validates input using CustomerCreate schema
@app.post("/customers", status_code=201)
def create_customer(customer: CustomerCreate):
    return {
        "message":"Customer Created",
        "data": customer
    }

# Get customer by ID (path parameter)
# order_id must be integer, otherwise FastAPI returns 422
@app.get("/customers/{customer_id}")
def get_customer(customer_id:int):
    return {
        "customer_id": customer_id,
        "name": "Sample user",
        "email": "sample@test.com"
    }

# Create a new product
# Validates price (float) and stock (int)
@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    return {
        "message": "Product Created",
        "data": product
    }

# Get product details by ID
@app.get("/products/{product_id}")
def get_product(product_id:int):
    return {
        "product_id": product_id,
        "name": "XYZ",
        "price": 2.345,
        "stock": 50
    }

# Create a new order
# Accepts nested items list (OrderItemCreate inside OrderCreate)
@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    return {
        "message": "Order Created",
        "order_id": 1,
        "customer_id": order.customer_id,
        "total_amount": "PENDING",
        "items": order.items
    }

# Get order details with items
# Combines order (header) + order_items (details)
@app.get("/orders/{order_id}")
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