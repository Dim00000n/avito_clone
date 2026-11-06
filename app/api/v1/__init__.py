from fastapi import APIRouter

from app.api.v1 import ads, search, users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(ads.router)
api_router.include_router(search.router)
