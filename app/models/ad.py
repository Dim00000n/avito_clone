from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Ad(Base):
    __tablename__ = "ads"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    price: Mapped[float] = mapped_column(Float)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category = relationship("Category", back_populates="ads")
    owner = relationship("User", back_populates="ads")
    # view_count: Mapped[int] = mapped_column(Integer)
    # is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    # is_adult = Mapped[bool] = mapped_column(Boolean, default=False)

