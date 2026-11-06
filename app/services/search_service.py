from sqlalchemy.orm import Session

from app.models import Ad
from app.repositories import ad_repo

SORTING = {
    "new": Ad.created_at.desc(),
    "price_asc": Ad.price.asc(),
    "price_desc": Ad.price.desc(),
}
def search_ads(db: Session, q, category_id, city, min_price, max_price, sort, skip, limit):
    total, items = ad_repo.search(
        db, q, category_id, city, min_price, max_price, SORTING[sort], skip, limit)
    return {"total": total, "items": items}
