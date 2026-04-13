from fastapi import APIRouter, HTTPException
from app.schemas import OrderCreate, OrderResponse
from app.database import SessionLocal
from app import models

router = APIRouter()

# # Create a new order
# # Accepts nested items list (OrderItemCreate inside OrderCreate)
@router.post("/orders", status_code=201, response_model=OrderResponse)
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

        # stored created order items for API response
        response_items = []

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

            #Add item details to response
            response_items.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": product.price,
                "subtotal": sub_total
            })
        
        # Update order header with final total amount
        new_order.total_amount = total_amount

        # Save order items + updated total
        db.commit()
        db.refresh(new_order)
       
        return {
            "order_id": new_order.id,
            "customer_id": new_order.customer_id,
            "status": new_order.status,
            "total_amount": new_order.total_amount,
            "items": response_items
        }
        

# Get order details with items
# Combines order (header) + order_items (details)
@router.get("/orders/{order_id}")
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