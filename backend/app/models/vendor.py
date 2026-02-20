from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Vendor(TimestampMixin, Base):
    """A vendor / stall holder at a local market."""

    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    stall_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    market_id: Mapped[int | None] = mapped_column(
        ForeignKey("markets.id", ondelete="SET NULL"), nullable=True, index=True
    )
    commodity_type: Mapped[str | None] = mapped_column(String(60), nullable=True)
    contact_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
