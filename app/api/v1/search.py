from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import ad_repo
from app.schemas.ad import AdList, CategoryOut
from app.services import search_service

router = APIRouter(tags=["Поиск"])


@router.get("/search", response_model=AdList)
def search(
    q: str | None = None,
    category_id: int | None = None,
    city: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort: Literal["new", "price_asc", "price_desc"] = "new",
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return search_service.search_ads(db, q, category_id, city, min_price, max_price, sort, skip, limit)


@router.get("/categories", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return ad_repo.get_categories(db)
