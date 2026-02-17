from datetime import date as dt_date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class DailyPrice(TimestampMixin, Base):
    __tablename__ = "daily_prices"
    __table_args__ = (
        UniqueConstraint(
            "commodity_id",
            "market_id",
            "date",
            "source",
            name="uq_daily_prices_commodity_market_date_source",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commodity_id: Mapped[int] = mapped_column(
        ForeignKey("commodities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id", ondelete="CASCADE"), nullable=False, index=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id", ondelete="CASCADE"), nullable=False, index=True)

    price_low: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    price_high: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    price_avg: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    price_prevailing: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    date: Mapped[dt_date] = mapped_column(Date, nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(40), nullable=False)
