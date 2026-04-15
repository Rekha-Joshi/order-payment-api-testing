from fastapi import APIRouter, HTTPException
from app.schemas import PaymentCreate
from app.database import SessionLocal
from app import models

router = APIRouter()

def get_order_or_404(db, order_id):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code = 404,
            detail = "Order not found."
        )
    return order

def validate_order_state(status):
    return status in ["PENDING", "FAILED"]

def get_payment_or_404(db, payment_id):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code = 404,
            detail = "Payment record not found."
        )
    return payment

@router.post("/payments", status_code=201)
def create_payment(payment: PaymentCreate):
    with SessionLocal() as db:

        #check if order exists else 404
        order = get_order_or_404(db, payment.order_id)

        #check order status
        if validate_order_state(order.status):
            if payment.amount == order.total_amount:
                new_payment = models.Payment(
                    order_id = payment.order_id,
                    amount = payment.amount,
                    status = "SUCCESS"
                )
                db.add(new_payment)
                order.status = "PAID"
            else:
                new_payment = models.Payment(
                    order_id = payment.order_id,
                    amount = payment.amount,
                    status = "FAILED"
                )
                db.add(new_payment)
                order.status = "FAILED"
        else:
            raise HTTPException(
                status_code = 400,
                detail = "Order is either already paid or cancelled."
            )
        db.commit()
        db.refresh(new_payment)
        return{
            "payment_id": new_payment.id,
            "order_id": new_payment.order_id,
            "amount": new_payment.amount,
            "status": new_payment.status
        }

@router.get("/payments/{payment_id}")
def read_payment(payment_id: int):
    with SessionLocal() as db:
        payment = get_payment_or_404(db, payment_id)
        return {
            "payment_id": payment.id,
            "order_id": payment.order_id,
            "amount": payment.amount,
            "status": payment.status
        }