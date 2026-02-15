from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class WeeklyVarianceResponse(BaseModel):
    week_start: date
    commodity_id: int
    commodity_name: str
    weekly_avg_price: Decimal
    wow_percent_change: float | None


class RegionalComparisonResponse(BaseModel):
    region_id: int
    region_name: str
    region_code: str
    avg_price: Decimal


class PriceSpikeResponse(BaseModel):
    commodity_id: int
    region_id: int
    date: date
    avg_price: Decimal
    rolling_mean_30: float | None
    rolling_std_30: float | None


class CheapestRegionResponse(BaseModel):
    commodity_id: int
    commodity_name: str
    region_id: int
    region_name: str
    region_code: str
    avg_price: Decimal
    date: date


class RollingAverageResponse(BaseModel):
    date: date
    avg_price: Decimal
    rolling_30_day_avg: float | None


class SeasonalPatternResponse(BaseModel):
    month: int
    avg_price: Decimal
