from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class DailyPriceResponse(BaseModel):
    id: int
    commodity_id: int
    market_id: int
    region_id: int
    price_low: Decimal | None
    price_high: Decimal | None
    price_avg: Decimal | None
    price_prevailing: Decimal
    date: date
    source: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LatestPriceResponse(BaseModel):
    commodity_id: int
    commodity_name: str
    commodity_category: str
    region_id: int
    region_code: str
    date: date
    avg_price: Decimal


class PriceHistoryResponse(BaseModel):
    date: date
    avg_price: Decimal
