from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class HarvestRecordCreate(BaseModel):
    region_id: int
    commodity_id: int
    quantity_kg: Decimal
    area_hectares: Decimal | None = None
    season: str | None = None
    harvest_date: date
    farmer_name: str | None = None
    notes: str | None = None


class HarvestRecordResponse(BaseModel):
    id: int
    region_id: int
    commodity_id: int
    quantity_kg: Decimal
    area_hectares: Decimal | None
    season: str
    harvest_date: date
    farmer_name: str | None
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class HarvestSummaryResponse(BaseModel):
    """Aggregate harvest totals per commodity + season."""
    commodity_id: int
    commodity_name: str
    season: str | None
    total_kg: float
    total_hectares: float | None
    record_count: int
