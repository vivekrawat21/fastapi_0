from fastapi import APIRouter, Depends, HTTPException, status
from app.database.connection.db_connection import get_db
from app.api.v1.schemas.Payments import PaymentCreate, PaymentResponse,PaymentUpdate
from app.database.crud import create_payment,get_payment_by_id,update_payment

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create( data: PaymentCreate, db=Depends(get_db)) -> PaymentResponse:
    """Create a new payment."""
    payment = await create_payment(db, data)
    if not payment:
        raise HTTPException(status_code=400, detail="Payment creation failed")
    return payment


@router.get("/{payment_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK)
async def get_payment(payment_id: int, db=Depends(get_db)) -> PaymentResponse:
    """Retrieve payment details by payment ID."""
    payment = await get_payment_by_id(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.put("/{payment_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK)
async def update_payment(payment_id: int, data: PaymentUpdate, db=Depends(get_db)) -> PaymentResponse:
    """Update an existing payment."""
    payment = await update_payment(db, payment_id, data)
    if not payment:
        raise HTTPException(status_code=400, detail="Payment update failed")
    return payment