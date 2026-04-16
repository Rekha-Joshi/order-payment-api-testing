from fastapi import APIRouter, HTTPException

from app.schemas import CustomerCreate
from app.database import SessionLocal
from app import models

router = APIRouter() # This is like mini FastAPI which only collects endpoints for customer only
#APIRouter helps organize endpoints by feature, and include_router registers those routes with the main FastAPI app

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