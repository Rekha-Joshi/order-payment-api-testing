from fastapi import APIRouter, HTTPException
from app.schemas import OrderCreate, OrderResponse
from app.database import SessionLocal
from app import models

router = APIRouter()

def get_customer_or_404(db, customer_id:int):
    # Check if customer exists
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    # Return 404 if Customer not found.
    if not customer: 
        raise HTTPException(
            status_code = 404,
            detail = "Customer not found."
        )
    return customer

def get_product_or_404(db, product_id:int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    # Return 404 if product not found
    if not product:
        raise HTTPException(
            status_code = 404,
            detail = f"Product {product_id} not found"
        )
    return product

def validate_stock(product, quantity:int):
    #Raise 400 if requested quantity is more than available stock
    if product.stock < quantity:
        raise HTTPException(
            status_code = 400,
            detail = f"Insufficient stock for product {product.id}"
        )

def create_order_header(db, customer_id:int):
    #create order header with temporary total_amount=0
    new_order = models.Order(
            customer_id = customer_id,
            status = "pending",
            total_amount = 0
        )
    db.add(new_order) #save order to DB
    db.flush() # Flush sends INSERT to DB and gets generated order id without committing the transaction yet
    return new_order

def create_order_items_and_calculate_total(db, order_id:int, items):
    # Track total order amount
    total_amount =0
    # stored created order items for API response
    response_items = []

    # Check if each product exists and has enough stock
    for item in items:
        #get product or raise 404
        product = get_product_or_404(db, item.product_id)

        # Return 400 if stock is not enough
        validate_stock(product, item.quantity)
        
        # Calculate subtotal for this item
        sub_total = product.price * item.quantity

        # Create order item
        new_order_item = models.OrderItem(
            order_id = order_id,
            product_id = item.product_id,
            quantity = item.quantity,
            price = product.price,
            subtotal = sub_total
        )

        db.add(new_order_item)

        #Reduce product stock
        product.stock -= item.quantity
        
        # Add subtotal to running total
        total_amount += sub_total

        # Build response items
        response_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": product.price,
            "subtotal": sub_total
        })
    return total_amount, response_items

def get_order_or_404(db, order_id:int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException (
            status_code = 404,
            detail = "Order not found."
        )
    return order

def get_order_items(db, order):
    order_items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order.id).all()
    if not order_items:
        raise HTTPException(
            status_code = 404,
            detail = "No items in this Order."
        )
    return order_items

def validate_cancel_order_status(status: str):
    if status == "pending":
        return True 
    elif status == "completed":
        raise HTTPException(
            status_code = 400,
            detail = "Order is already completed and can't be cancelled."
        )
    elif status == "cancelled":
        raise HTTPException(
            status_code = 400,
            detail = "Order is already cancelled."
        )
    else:
        raise HTTPException(
            status_code = 400,
            detail = "Invalid order status."
        )

# Accepts nested items list (OrderItemCreate inside OrderCreate)
@router.post("/orders", status_code=201, response_model=OrderResponse)
def create_order(order: OrderCreate):
    with SessionLocal() as db:
        
        customer = get_customer_or_404(db, order.customer_id)
        new_order = create_order_header(db, order.customer_id)

        total_amount , response_items = create_order_items_and_calculate_total(db, new_order.id, order.items)
        
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
@router.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int):
    with SessionLocal() as db:
        order = get_order_or_404(db, order_id)

        # Fetch order items and format for response
        order_items = get_order_items(db, order)
        response_items = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.subtotal
            } for item in order_items
        ]
        return {
            "order_id": order.id,
            "customer_id": order.customer_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "items": response_items
        }

@router.patch("/orders/{order_id}/cancel")
def updated_order(order_id: int):
    with SessionLocal() as db:
        order = get_order_or_404(db, order_id)
        if validate_cancel_order_status(order.status):
            # allow cancel. Get all the items of this order
            items = get_order_items(db, order)

            # once we have all items, go through them to get product_id and update the stock
            for item in items:
                product = get_product_or_404(db, item.product_id)
                product.stock += item.quantity
            order.status = "cancelled"
        db.commit()
        db.refresh(order)
        return {
            "order_id": order_id,
            "customer_id": order.customer_id,
            "status": order.status,
            "total_amount": order.total_amount
        }