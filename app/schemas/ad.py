from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class AdCreate(BaseModel):
    title: str
    description: str = ""
    price: float
    city: str | None = None
    category_id: int
    owner_id: int


class AdUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    city: str | None = None
    category_id: int | None = None
    is_active: bool | None = None


class AdOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    price: float
    city: str | None
    is_active: bool
    created_at: datetime
    category_id: int
    owner_id: int


class AdList(BaseModel):
    total: int
    items: list[AdOut]
