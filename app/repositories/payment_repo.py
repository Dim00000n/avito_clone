from sqlalchemy.orm import Session

from app.models import Payment


def create(db: Session, data: dict) -> Payment:
    payment = Payment(**data)
    db.add(payment)
    db.flush()
    return payment


def get_all_for_user(db: Session, user_id: int) -> list[Payment]:
    return list(
        db.query(Payment)
        .filter((Payment.buyer_id == user_id) | (Payment.seller_id == user_id))
        .order_by(Payment.created_at.desc())
        .all()
    )
