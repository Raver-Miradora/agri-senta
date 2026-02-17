"""Shared fixtures for backend integration tests.

Uses an async in-memory SQLite database so tests don't need PostgreSQL.
The FastAPI app's DB dependency is overridden to point at this test DB.
"""

from collections.abc import AsyncGenerator
from datetime import date, datetime, timedelta
from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.database import get_db_session
from app.models import Commodity, DailyPrice, Market, PriceForecast, Region
from app.models.base import Base

# ---------------------------------------------------------------------------
# Engine & session factory – in-memory SQLite with StaticPool
# so all connections share the same underlying database.
# ---------------------------------------------------------------------------
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DB_URL,
    echo=False,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create tables, yield a session, then tear everything down."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def seeded_session(db_session: AsyncSession) -> AsyncSession:
    """Session pre-loaded with sample commodities, regions, a market, prices, and forecasts."""
    # -- Regions --
    r1 = Region(id=1, name="National Capital Region", code="NCR", island_group="Luzon")
    r2 = Region(id=2, name="Region III - Central Luzon", code="R03", island_group="Luzon")
    db_session.add_all([r1, r2])
    await db_session.flush()

    # -- Market --
    m1 = Market(id=1, name="Quezon City Public Market", region_id=1, type="public")
    m2 = Market(id=2, name="Pampanga Public Market", region_id=2, type="public")
    db_session.add_all([m1, m2])
    await db_session.flush()

    # -- Commodities --
    c1 = Commodity(id=1, name="Well-Milled Rice", category="Rice", unit="kg")
    c2 = Commodity(id=2, name="Red Onion", category="Vegetables", unit="kg")
    c3 = Commodity(id=3, name="Pork Liempo", category="Meat", unit="kg")
    db_session.add_all([c1, c2, c3])
    await db_session.flush()

    # -- Daily prices (30 days for commodity 1, region 1) --
    today = date(2026, 2, 15)
    for i in range(30):
        d = today - timedelta(days=29 - i)
        price = Decimal("48.00") + Decimal(str(round(i * 0.1, 2)))
        dp = DailyPrice(
            commodity_id=1,
            market_id=1,
            region_id=1,
            price_low=price - Decimal("2.00"),
            price_high=price + Decimal("2.00"),
            price_avg=price,
            price_prevailing=price,
            date=d,
            source="DA-BPI",
        )
        db_session.add(dp)

    # -- A few prices for commodity 2 --
    for i in range(10):
        d = today - timedelta(days=9 - i)
        price = Decimal("130.00") + Decimal(str(round(i * 0.5, 2)))
        dp = DailyPrice(
            commodity_id=2,
            market_id=1,
            region_id=1,
            price_low=price - Decimal("5.00"),
            price_high=price + Decimal("5.00"),
            price_avg=price,
            price_prevailing=price,
            date=d,
            source="DA-BPI",
        )
        db_session.add(dp)

    # -- Prices for commodity 1, region 2 (for regional comparison) --
    for i in range(10):
        d = today - timedelta(days=9 - i)
        price = Decimal("50.00") + Decimal(str(round(i * 0.15, 2)))
        dp = DailyPrice(
            commodity_id=1,
            market_id=2,
            region_id=2,
            price_low=price - Decimal("2.00"),
            price_high=price + Decimal("2.00"),
            price_avg=price,
            price_prevailing=price,
            date=d,
            source="DA-BPI",
        )
        db_session.add(dp)

    await db_session.flush()

    # -- Forecasts --
    for i in range(7):
        fc = PriceForecast(
            commodity_id=1,
            region_id=1,
            forecast_date=today + timedelta(days=i + 1),
            predicted_price=Decimal("51.00") + Decimal(str(round(i * 0.2, 2))),
            confidence_lower=Decimal("49.00"),
            confidence_upper=Decimal("53.00"),
            model_used="linear_regression",
            generated_at=datetime(2026, 2, 15, 0, 0, 0),
        )
        db_session.add(fc)

    await db_session.commit()
    return db_session


@pytest.fixture()
async def client(seeded_session: AsyncSession):
    """AsyncClient wired to the FastAPI app with the DB dependency overridden."""
    from app.main import app

    async def _override_db() -> AsyncGenerator[AsyncSession, None]:
        yield seeded_session

    app.dependency_overrides[get_db_session] = _override_db

    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
