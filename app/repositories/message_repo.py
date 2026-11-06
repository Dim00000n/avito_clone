from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Message


def create(db: Session, data: dict) -> Message:
    msg = Message(**data)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_all(db: Session) -> list[Message]:
    return list(db.scalars(select(Message).order_by(Message.id.desc())))
