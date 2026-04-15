from fastapi import FastAPI, HTTPException

# Import request validation schemas (Pydantic models)
from app.routers import customers, products, orders, payments

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

app.include_router(customers.router) #This tells FastAPI that take all endpoints in this router and attach them to main app.
#APIRouter helps organize endpoints by feature, and include_router registers those routes with the main FastAPI app

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payments.router)