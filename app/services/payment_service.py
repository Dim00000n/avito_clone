from decimal import Decimal, InvalidOperation

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Ad, User
from app.repositories import payment_repo


def _money(value) -> Decimal:
    try:
        amount = Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        raise HTTPException(400, "Некорректная сумма")
    if amount <= 0:
        raise HTTPException(400, "Сумма должна быть больше нуля")
    return amount


def deposit(db: Session, user_id: int, raw_amount) -> User:
    amount = _money(raw_amount)
    try:
        result = db.execute(
            update(User)
            .where(User.id == user_id)
            .values(balance=User.balance + amount)
        )
        if result.rowcount != 1:
            db.rollback()
            raise HTTPException(404, "Пользователь не найден")
        db.commit()
    except Exception:
        db.rollback()
        raise
    return db.get(User, user_id)


def purchase(db: Session, ad_id: int, buyer_id: int):
    try:
        ad = db.get(Ad, ad_id)
        if ad is None:
            raise HTTPException(404, "Объявление не найдено")
        if not ad.is_active:
            raise HTTPException(409, "Объявление уже продано или неактивно")
        if ad.owner_id == buyer_id:
            raise HTTPException(400, "Нельзя купить собственное объявление")

        amount = _money(ad.price)
        seller_id = ad.owner_id

        debit = db.execute(
            update(User)
            .where(User.id == buyer_id, User.balance >= amount)
            .values(balance=User.balance - amount)
        )
        if debit.rowcount != 1:
            buyer_exists = db.get(User, buyer_id)
            if buyer_exists is None:
                raise HTTPException(404, "Покупатель не найден")
            raise HTTPException(400, "Недостаточно средств на балансе")

        claim = db.execute(
            update(Ad)
            .where(Ad.id == ad_id, Ad.is_active.is_(True))
            .values(is_active=False)
        )
        if claim.rowcount != 1:
            raise HTTPException(409, "Объявление уже куплено")

        credit = db.execute(
            update(User)
            .where(User.id == seller_id)
            .values(balance=User.balance + amount)
        )
        if credit.rowcount != 1:
            raise HTTPException(404, "Продавец не найден")

        payment = payment_repo.create(
            db,
            {
                "buyer_id": buyer_id,
                "seller_id": seller_id,
                "ad_id": ad_id,
                "amount": amount,
            },
        )
        db.commit()
        db.refresh(payment)
        return payment
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Это объявление уже было оплачено")
    except Exception:
        db.rollback()
        raise
