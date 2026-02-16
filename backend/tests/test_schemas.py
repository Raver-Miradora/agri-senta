from app.schemas.price import DailyPriceResponse, LatestPriceResponse, PriceHistoryResponse
from app.schemas.analytics import WeeklyVarianceResponse, RegionalComparisonResponse, PriceSpikeResponse
from app.schemas.forecast import ForecastPointResponse, ForecastSummaryResponse
from app.schemas.commodity import CommodityResponse
from app.schemas.region import RegionResponse

from datetime import date, datetime
from decimal import Decimal


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


def test_latest_price_response_fields() -> None:
    obj = LatestPriceResponse(
        commodity_id=2,
        commodity_name="Red Onion",
        region_id=1,
        region_code="NCR",
        date=date(2026, 1, 15),
        avg_price=Decimal("130.00"),
    )
    assert obj.commodity_name == "Red Onion"


def test_weekly_variance_response_nullable_change() -> None:
    obj = WeeklyVarianceResponse(
        week_start=date(2026, 1, 6),
        commodity_id=1,
        commodity_name="Well-Milled Rice",
        weekly_avg_price=Decimal("48.50"),
        wow_percent_change=None,
    )
    assert obj.wow_percent_change is None


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
