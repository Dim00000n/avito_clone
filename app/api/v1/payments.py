from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.payment import BalanceDeposit, BalanceOut, PaymentOut, PurchaseCreate
from app.services import payment_service

router = APIRouter(prefix="/payments", tags=["Тестовая оплата"])


@router.post("/deposit", response_model=BalanceOut, summary="Тестовое пополнение баланса")
def deposit(data: BalanceDeposit, db: Session = Depends(get_db)):
    user = payment_service.deposit(db, data.user_id, data.amount)
    return {"user_id": user.id, "balance": user.balance}


@router.post("/purchase/{ad_id}", response_model=PaymentOut, status_code=201,
             summary="Купить объявление с баланса")
def purchase(ad_id: int, data: PurchaseCreate, db: Session = Depends(get_db)):
    return payment_service.purchase(db, ad_id, data.buyer_id)
