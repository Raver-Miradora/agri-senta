from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class PriceAlert(TimestampMixin, Base):
    """Triggered when a commodity price deviates beyond a threshold."""

    __tablename__ = "price_alerts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commodity_id: Mapped[int] = mapped_column(
        ForeignKey("commodities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    region_id: Mapped[int | None] = mapped_column(
        ForeignKey("regions.id", ondelete="SET NULL"), nullable=True, index=True
    )
    alert_type: Mapped[str] = mapped_column(String(30), nullable=False)  # spike, drop, ceiling_breach
    severity: Mapped[str] = mapped_column(String(15), nullable=False, default="medium")  # low, medium, high
    current_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    threshold_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    triggered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_resolved: Mapped[bool] = mapped_column(default=False, nullable=False)
