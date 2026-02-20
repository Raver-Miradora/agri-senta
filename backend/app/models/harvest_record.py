from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class HarvestRecord(TimestampMixin, Base):
    """Records crop harvest yields per barangay/commodity/season."""

    __tablename__ = "harvest_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    commodity_id: Mapped[int] = mapped_column(
        ForeignKey("commodities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    quantity_kg: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    area_hectares: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    season: Mapped[str | None] = mapped_column(String(30), nullable=True)  # e.g. "Dry", "Wet", "Year-Round"
    harvest_date: Mapped[date] = mapped_column(Date, nullable=False)
    farmer_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
