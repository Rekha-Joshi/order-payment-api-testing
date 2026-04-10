from http.client import HTTP_PORT

from fastapi import FastAPI, HTTPException

# Import request validation schemas (Pydantic models)
from app.schemas import CustomerCreate, ProductCreate, OrderCreate, OrderItemCreate

# Import database engine and models
from app.database import engine, Base, SessionLocal
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
    # Open database session
    with SessionLocal() as db: # earlier db = SessionLocal()
        
        # Create Customer ORM object from request data
        new_customer = models.Customer( #creating new instance of Customer class from models
            name = customer.name,
            email = customer.email
        )
        
        # Add and save customer to PostgreSQL
        db.add(new_customer) #prepare db insert
        db.commit()
        db.refresh(new_customer) #reloads object from DB, so that generated field like id and created_at comes back
        #db.close() #close the connection. Not needed any more as we are using with command now
        
        return {
            "id": new_customer.id,
            "name": new_customer.name,
            "email": new_customer.email,
            "created_at": new_customer.created_at
        }

# Get customer by ID (path parameter)
# customer_id must be integer, otherwise FastAPI returns 422
@app.get("/customers/{customer_id}")
def get_customer(customer_id:int):
    with SessionLocal() as db:
        
        customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if not customer:
            raise HTTPException (
                status_code = 404,
                detail = "Customer not found."
            )
        
        return {
            "id": customer_id,
            "name": customer.name,
            "email": customer.email,
            "created_at": customer.created_at
        }

# Create a new product
# Validates price (float) and stock (int)
@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    with SessionLocal() as db:
        
        new_product = models.Product(
            name = product.name,
            price = product.price,
            stock = product.stock
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        return {
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price,
            "stock": new_product.stock,
            "created_at": new_product.created_at
        }

# Get product details by ID
@app.get("/products/{product_id}")
def get_product(product_id:int):
    with SessionLocal() as db:

        product = db.query(models.Product).filter(models.Product.id == product_id).first()

        if not product:
            raise HTTPException(
                status_code = 404,
                detail = "Product not found."
            )
        
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        }

# Create a new order
# Accepts nested items list (OrderItemCreate inside OrderCreate)
@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    with SessionLocal() as db:
        # Check if customer exists
        customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
        # Return 404 if Customer not found.
        if not customer: 
            raise HTTPException(
                status_code = 404,
                detail = "Customer not found."
            )
        # create order header first
        new_order = models.Order(
            customer_id = order.customer_id,
            status = "PENDING",
            total_amount = 0
        )

        #save order to DB
        db.add(new_order)
        # Flush sends INSERT to DB and gets generated order id
        # without committing the transaction yet
        db.flush()

         # Track total order amount
        total_amount =0

        # Check if each product exists and has enough stock
        for item in order.items:
            product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
            # Return 404 if product not found
            if not product:
                raise HTTPException(
                    status_code = 404,
                    detail = f"Product {item.product_id} not found"
                )
            # Return 400 if stock is not enough
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code = 400,
                    detail = f"Insufficient stock for product {item.product_id}"
                )
            # Calculate subtotal for this item
            sub_total = product.price * item.quantity

            #reduce product stock
            product.stock -= item.quantity

            #Create order item
            new_order_item = models.OrderItem(
                order_id = new_order.id,
                product_id = item.product_id,
                quantity = item.quantity,
                price = product.price,
                subtotal = sub_total
            )
            db.add(new_order_item)

            # Add subtotal to running total
            total_amount += sub_total
        
        # Update order header with final total amount
        new_order.total_amount = total_amount

        # Save order items + updated total
        db.commit()
        db.refresh(new_order)
       
        return {
            "message": "Order header created successfully",
            "order_id": new_order.id,
            "customer_id": new_order.customer_id,
            "status": new_order.status,
            "total_amount": new_order.total_amount
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