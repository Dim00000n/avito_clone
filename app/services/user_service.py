from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import user_repo
from app.schemas.user import UserCreate


def create_user(db: Session, data: UserCreate):
    if user_repo.get_by_email(db, data.email):
        raise HTTPException(400, "Пользователь с таким email уже есть")
    return user_repo.create(db, data.model_dump())


def get_user(db: Session, user_id: int):
    user = user_repo.get(db, user_id)
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    return user


def get_users(db: Session):
    return user_repo.get_all(db)
