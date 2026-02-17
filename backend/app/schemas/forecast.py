from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class ForecastPointResponse(BaseModel):
    commodity_id: int
    region_id: int
    forecast_date: date
    predicted_price: Decimal
    confidence_lower: Decimal | None
    confidence_upper: Decimal | None
    model_used: str
    generated_at: datetime

    model_config = {"from_attributes": True}


class ForecastSummaryResponse(BaseModel):
    commodity_id: int
    commodity_name: str
    commodity_category: str
    region_id: int
    region_code: str
    forecast_date: date
    predicted_price: Decimal
    model_used: str
