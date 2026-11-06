from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories import ad_repo, user_repo
from app.schemas.ad import AdCreate, AdUpdate

def create_ad(db: Session, data: AdCreate):
    if not user_repo.get(db, data.owner_id):
        raise HTTPException(400, "Пользователь (owner_id) не найден")
    if not ad_repo.get_category(db, data.category_id):
        raise HTTPException(400, "Категория (category_id) не найдена")
    return ad_repo.create(db, data.model_dump())
def get_ad(db: Session, ad_id: int):
    ad = ad_repo.get(db, ad_id)
    if not ad:
        raise HTTPException(404, "Объявление не найдено")
    return ad
def get_ads(db: Session):
    return ad_repo.get_all(db)
def update_ad(db: Session, ad_id: int, data: AdUpdate):
    ad = get_ad(db, ad_id)
    return ad_repo.update(db, ad, data.model_dump(exclude_unset=True))
def delete_ad(db: Session, ad_id: int):
    ad_repo.delete(db, get_ad(db, ad_id))
