from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ad import AdCreate, AdOut, AdUpdate
from app.services import ad_service

router = APIRouter(prefix="/ads", tags=["Объявления"])


@router.post("", response_model=AdOut, status_code=201)
def create_ad(data: AdCreate, db: Session = Depends(get_db)):
    return ad_service.create_ad(db, data)


@router.get("", response_model=list[AdOut])
def get_ads(db: Session = Depends(get_db)):
    return ad_service.get_ads(db)


@router.get("/{ad_id}", response_model=AdOut)
def get_ad(ad_id: int, db: Session = Depends(get_db)):
    return ad_service.get_ad(db, ad_id)


@router.patch("/{ad_id}", response_model=AdOut)
def update_ad(ad_id: int, data: AdUpdate, db: Session = Depends(get_db)):
    return ad_service.update_ad(db, ad_id, data)


@router.delete("/{ad_id}", status_code=204)
def delete_ad(ad_id: int, db: Session = Depends(get_db)):
    ad_service.delete_ad(db, ad_id)
