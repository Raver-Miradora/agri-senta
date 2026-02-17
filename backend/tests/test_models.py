"""Tests for SQLAlchemy models – basic instantiation & field validation."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import select

from app.models import Commodity, DailyPrice, Market, PriceForecast, Region
from app.models.scrape_log import ScrapeLog


async def test_commodity_creation(db_session):
    c = Commodity(name="Test Commodity", category="Vegetables", unit="kg")
    db_session.add(c)
    await db_session.commit()

    result = await db_session.execute(select(Commodity).where(Commodity.name == "Test Commodity"))
    row = result.scalar_one()
    assert row.category == "Vegetables"
    assert row.unit == "kg"
    assert row.image_url is None


async def test_region_creation(db_session):
    r = Region(name="Test Region", code="TR01", island_group="Luzon")
    db_session.add(r)
    await db_session.commit()

    result = await db_session.execute(select(Region).where(Region.code == "TR01"))
    row = result.scalar_one()
    assert row.island_group == "Luzon"


async def test_market_requires_region(db_session):
    r = Region(id=99, name="Test Region", code="TR99", island_group="Visayas")
    db_session.add(r)
    await db_session.flush()

    m = Market(name="Test Market", region_id=99, type="public")
    db_session.add(m)
    await db_session.commit()

    result = await db_session.execute(select(Market).where(Market.name == "Test Market"))
    row = result.scalar_one()
    assert row.region_id == 99
    assert row.type == "public"


async def test_daily_price_fields(db_session):
    r = Region(id=1, name="NCR", code="NCR", island_group="Luzon")
    c = Commodity(id=1, name="Rice", category="Rice", unit="kg")
    m = Market(id=1, name="QC Market", region_id=1, type="public")
    db_session.add_all([r, c, m])
    await db_session.flush()

    dp = DailyPrice(
        commodity_id=1,
        market_id=1,
        region_id=1,
        price_low=Decimal("45.00"),
        price_high=Decimal("50.00"),
        price_avg=Decimal("47.50"),
        price_prevailing=Decimal("48.00"),
        date=date(2026, 2, 1),
        source="DA-BPI",
    )
    db_session.add(dp)
    await db_session.commit()

    result = await db_session.execute(select(DailyPrice))
    row = result.scalar_one()
    assert row.source == "DA-BPI"
    assert row.price_prevailing == Decimal("48.00")


async def test_price_forecast_fields(db_session):
    r = Region(id=1, name="NCR", code="NCR", island_group="Luzon")
    c = Commodity(id=1, name="Rice", category="Rice", unit="kg")
    db_session.add_all([r, c])
    await db_session.flush()

    fc = PriceForecast(
        commodity_id=1,
        region_id=1,
        forecast_date=date(2026, 2, 20),
        predicted_price=Decimal("50.00"),
        confidence_lower=Decimal("48.00"),
        confidence_upper=Decimal("52.00"),
        model_used="linear_regression",
        generated_at=datetime(2026, 2, 19, 0, 0, 0),
    )
    db_session.add(fc)
    await db_session.commit()

    result = await db_session.execute(select(PriceForecast))
    row = result.scalar_one()
    assert row.model_used == "linear_regression"


async def test_scrape_log_fields(db_session):
    log = ScrapeLog(
        source="DA",
        status="success",
        rows_ingested=100,
        duration_seconds=5.2,
    )
    db_session.add(log)
    await db_session.commit()

    result = await db_session.execute(select(ScrapeLog))
    row = result.scalar_one()
    assert row.source == "DA"
    assert row.rows_ingested == 100
    assert row.error_message is None
