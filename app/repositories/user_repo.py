from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def get(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def get_all(db: Session) -> list[User]:
    return list(db.scalars(select(User)))


def create(db: Session, data: dict) -> User:
    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
