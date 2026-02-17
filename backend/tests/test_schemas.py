"""Tests for Pydantic response schemas – instantiation & field validation."""

from datetime import date, datetime
from decimal import Decimal

from app.schemas.admin import ScrapeLogResponse, ScrapeTriggerResponse
from app.schemas.analytics import (
    CheapestRegionResponse,
    PriceSpikeResponse,
    RegionalComparisonResponse,
    RollingAverageResponse,
    SeasonalPatternResponse,
    WeeklyVarianceResponse,
)
from app.schemas.commodity import CommodityResponse
from app.schemas.forecast import ForecastPointResponse, ForecastSummaryResponse
from app.schemas.price import DailyPriceResponse, LatestPriceResponse, PriceHistoryResponse
from app.schemas.region import RegionResponse

# --------------- Price schemas ---------------


def test_daily_price_response_from_attributes() -> None:
    obj = DailyPriceResponse(
        id=1,
        commodity_id=1,
        market_id=1,
        region_id=1,
        price_low=Decimal("45.00"),
        price_high=Decimal("50.00"),
        price_avg=Decimal("47.50"),
        price_prevailing=Decimal("48.00"),
        date=date(2026, 1, 15),
        source="DA",
        created_at=datetime(2026, 1, 15, 6, 0, 0),
    )
    assert obj.price_prevailing == Decimal("48.00")
    assert obj.source == "DA"


def test_latest_price_response_includes_category() -> None:
    obj = LatestPriceResponse(
        commodity_id=2,
        commodity_name="Red Onion",
        commodity_category="Vegetables",
        region_id=1,
        region_code="NCR",
        date=date(2026, 1, 15),
        avg_price=Decimal("130.00"),
    )
    assert obj.commodity_name == "Red Onion"
    assert obj.commodity_category == "Vegetables"


def test_price_history_response() -> None:
    obj = PriceHistoryResponse(
        date=date(2026, 2, 1),
        avg_price=Decimal("48.00"),
    )
    assert obj.avg_price == Decimal("48.00")


# --------------- Analytics schemas ---------------


def test_weekly_variance_response_nullable_change() -> None:
    obj = WeeklyVarianceResponse(
        week_start=date(2026, 1, 6),
        commodity_id=1,
        commodity_name="Well-Milled Rice",
        weekly_avg_price=Decimal("48.50"),
        wow_percent_change=None,
    )
    assert obj.wow_percent_change is None


def test_regional_comparison_response() -> None:
    obj = RegionalComparisonResponse(
        region_id=1,
        region_name="NCR",
        region_code="NCR",
        avg_price=Decimal("48.00"),
    )
    assert obj.region_code == "NCR"


def test_price_spike_response() -> None:
    obj = PriceSpikeResponse(
        commodity_id=1,
        region_id=1,
        date=date(2026, 2, 10),
        avg_price=Decimal("65.00"),
        rolling_mean_30=48.5,
        rolling_std_30=2.1,
    )
    assert obj.avg_price == Decimal("65.00")
    assert obj.rolling_mean_30 == 48.5


def test_cheapest_region_response() -> None:
    obj = CheapestRegionResponse(
        commodity_id=1,
        commodity_name="Well-Milled Rice",
        region_id=2,
        region_name="Region III",
        region_code="R03",
        avg_price=Decimal("46.00"),
        date=date(2026, 2, 15),
    )
    assert obj.region_code == "R03"


def test_rolling_average_response() -> None:
    obj = RollingAverageResponse(
        date=date(2026, 2, 15),
        avg_price=Decimal("48.00"),
        rolling_30_day_avg=47.8,
    )
    assert obj.rolling_30_day_avg == 47.8


def test_seasonal_pattern_response() -> None:
    obj = SeasonalPatternResponse(month=1, avg_price=Decimal("48.00"))
    assert obj.month == 1


# --------------- Forecast schemas ---------------


def test_forecast_point_response_model_validate() -> None:
    data = {
        "commodity_id": 1,
        "region_id": 1,
        "forecast_date": date(2026, 1, 20),
        "predicted_price": Decimal("50.00"),
        "confidence_lower": Decimal("48.00"),
        "confidence_upper": Decimal("52.00"),
        "model_used": "linear_regression",
        "generated_at": datetime(2026, 1, 19, 0, 0, 0),
    }
    obj = ForecastPointResponse.model_validate(data)
    assert obj.model_used == "linear_regression"


def test_forecast_summary_response_includes_category() -> None:
    obj = ForecastSummaryResponse(
        commodity_id=1,
        commodity_name="Well-Milled Rice",
        commodity_category="Rice",
        region_id=1,
        region_code="NCR",
        forecast_date=date(2026, 2, 20),
        predicted_price=Decimal("51.00"),
        model_used="linear_regression",
    )
    assert obj.commodity_category == "Rice"
    assert obj.model_used == "linear_regression"


# --------------- Commodity & Region schemas ---------------


def test_commodity_response_image_url_optional() -> None:
    obj = CommodityResponse(
        id=1,
        name="Well-Milled Rice",
        category="Rice",
        unit="kg",
        image_url=None,
        created_at=datetime(2026, 1, 1, 0, 0, 0),
    )
    assert obj.image_url is None


def test_region_response_fields() -> None:
    obj = RegionResponse(
        id=1,
        name="National Capital Region",
        code="NCR",
        island_group="Luzon",
        created_at=datetime(2026, 1, 1, 0, 0, 0),
    )
    assert obj.island_group == "Luzon"


# --------------- Admin schemas ---------------


def test_scrape_trigger_response() -> None:
    obj = ScrapeTriggerResponse(
        status="success",
        source="DA",
        rows_ingested=150,
    )
    assert obj.rows_ingested == 150


def test_scrape_log_response() -> None:
    obj = ScrapeLogResponse(
        id=1,
        source="DA",
        status="success",
        rows_ingested=100,
        error_message=None,
        duration_seconds=3.5,
        executed_at=datetime(2026, 2, 15, 6, 0, 0),
    )
    assert obj.error_message is None
    assert obj.duration_seconds == 3.5
