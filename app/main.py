from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app import models
from app.api.v1 import api_router
from app.config import APP_NAME, CORS_ORIGINS
from app.database import Base, SessionLocal, engine


def seed_demo_data():
    with SessionLocal() as db:
        if db.query(models.Category).count():
            return
        cats = [models.Category(name=n) for n in
                ["Транспорт", "Недвижимость", "Электроника", "Одежда", "Услуги"]]
        user = models.User(username="Иван", email="ivan@example.com", phone="+79990000000")
        db.add_all(cats + [user])
        db.commit()
        db.add_all([
            models.Ad(title="iPhone 13", description="Как новый", price=45000,
                      city="Москва", category_id=cats[2].id, owner_id=user.id),
            models.Ad(title="Велосипед горный", description="Почти не катался", price=15000,
                      city="Казань", category_id=cats[0].id, owner_id=user.id),
            models.Ad(title="Куртка зимняя", description="Размер L", price=3000,
                      city="Москва", category_id=cats[3].id, owner_id=user.id),
        ])
        db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_demo_data()
    yield


app = FastAPI(title=APP_NAME, lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])

app.include_router(api_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")
