from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import Ad, Category


def get(db: Session, ad_id: int) -> Ad | None:
    return db.get(Ad, ad_id)


def get_all(db: Session) -> list[Ad]:
    return list(db.scalars(select(Ad).order_by(Ad.id.desc())))


def create(db: Session, data: dict) -> Ad:
    ad = Ad(**data)
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad


def update(db: Session, ad: Ad, data: dict) -> Ad:
    for key, value in data.items():
        setattr(ad, key, value)
    db.commit()
    db.refresh(ad)
    return ad


def delete(db: Session, ad: Ad) -> None:
    db.delete(ad)
    db.commit()


def search(db: Session, q, category_id, city, min_price, max_price, order_by, skip, limit):
    stmt = select(Ad).where(Ad.is_active.is_(True))
    if q:
        like = f"%{q.lower()}%"
        stmt = stmt.where(or_(func.lower(Ad.title).like(like), func.lower(Ad.description).like(like)))
    if category_id:
        stmt = stmt.where(Ad.category_id == category_id)
    if city:
        stmt = stmt.where(func.lower(Ad.city) == city.lower())
    if min_price is not None:
        stmt = stmt.where(Ad.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Ad.price <= max_price)

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = list(db.scalars(stmt.order_by(order_by).offset(skip).limit(limit)))
    return total, items


def get_category(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def get_categories(db: Session) -> list[Category]:
    return list(db.scalars(select(Category)))
