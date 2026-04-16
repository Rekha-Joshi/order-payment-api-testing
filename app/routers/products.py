from fastapi import APIRouter, HTTPException
from app.schemas import ProductCreate
from app.database import SessionLocal
from app import models

router = APIRouter()

#Create a new product. Validates price (float) and stock (int)
@router.post("/products", status_code=201)
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
@router.get("/products/{product_id}")
def read_product(product_id:int):
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