from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BalanceDeposit(BaseModel):
    user_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class PurchaseCreate(BaseModel):
    buyer_id: int = Field(gt=0)


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    buyer_id: int
    seller_id: int
    ad_id: int
    amount: Decimal
    created_at: datetime


class BalanceOut(BaseModel):
    user_id: int
    balance: Decimal
