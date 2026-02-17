from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PriceForecast(Base):
    __tablename__ = "price_forecasts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commodity_id: Mapped[int] = mapped_column(
        ForeignKey("commodities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id", ondelete="CASCADE"), nullable=False, index=True)
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    predicted_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    confidence_lower: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    confidence_upper: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    model_used: Mapped[str] = mapped_column(String(50), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
