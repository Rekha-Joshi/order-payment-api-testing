from fastapi import APIRouter, HTTPException

from app.schemas import CustomerCreate
from app.database import SessionLocal
from app import models

router = APIRouter() # This is like mini FastAPI which only collects endpoints for customer only
#APIRouter helps organize endpoints by feature, and include_router registers those routes with the main FastAPI app

def get_customer_or_404(db, customer_id:int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code = 404,
            detail = "Customer not found."
        )
    return customer

def get_orders_or_404(db, customer_id:int):
    orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()
    if not orders:
        raise HTTPException(
            status_code = 404,
            detail = f"No orders for customer: {customer_id}."
        )
    return orders

def get_order_items(db, order_id):
    items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
    if not items:
        raise HTTPException(
            status_code = 404,
            detail = f"No items found for order id: {order_id}."
        )
    return items

# Create a new customer
# FastAPI validates input using CustomerCreate schema
@router.post("/customers", status_code=201)
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
        
        return {
            "id": new_customer.id,
            "name": new_customer.name,
            "email": new_customer.email,
            "created_at": new_customer.created_at
        }

# Get customer by ID (path parameter)
# customer_id must be integer, otherwise FastAPI returns 422
@router.get("/customers/{customer_id}")
def read_customer(customer_id:int):
    with SessionLocal() as db:
        
        customer = get_customer_or_404(db, customer_id)
        return {
            "id": customer_id,
            "name": customer.name,
            "email": customer.email,
            "created_at": customer.created_at
        }

# get the order and ites items for the customer
@router.get("/customers/{customer_id}/orders")
def read_customer_order(customer_id: int):
    with SessionLocal() as db:
        get_customer_or_404(db, customer_id)
        orders = get_orders_or_404(db, customer_id)       
        customer_orders = []

        for order in orders:
            items = get_order_items(db, order.id)
            response_items = [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price,
                    "subtotal": item.subtotal
                }for item in items
            ]
            customer_orders.append({
                "customer_id": customer_id,
                "order_id": order.id,
                "status": order.status,
                "total_amount": order.total_amount,
                "items": response_items
            })
        return customer_orders