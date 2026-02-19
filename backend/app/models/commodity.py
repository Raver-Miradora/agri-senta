from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Commodity(TimestampMixin, Base):
    __tablename__ = "commodities"
    __table_args__ = (
        Index("ix_commodities_category", "category"),
        Index("ix_commodities_name_lower", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
