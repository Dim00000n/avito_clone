from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: str
    phone: str | None = None


class UserOut(UserCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    balance: Decimal
