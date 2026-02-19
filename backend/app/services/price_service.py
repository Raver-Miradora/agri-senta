from datetime import date

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Commodity, DailyPrice, Region


async def get_daily_prices(
    session: AsyncSession,
    *,
    commodity_id: int | None,
    region_id: int | None,
    from_date: date | None,
    to_date: date | None,
    limit: int,
) -> list[DailyPrice]:
    statement: Select[tuple[DailyPrice]] = select(DailyPrice).order_by(DailyPrice.date.desc(), DailyPrice.id.desc())

    if commodity_id is not None:
        statement = statement.where(DailyPrice.commodity_id == commodity_id)
    if region_id is not None:
        statement = statement.where(DailyPrice.region_id == region_id)
    if from_date is not None:
        statement = statement.where(DailyPrice.date >= from_date)
    if to_date is not None:
        statement = statement.where(DailyPrice.date <= to_date)

    result = await session.execute(statement.limit(limit))
    return list(result.scalars().all())


def _build_latest_base_query(
    *,
    search: str | None = None,
    category: str | None = None,
    region_id: int | None = None,
):
    """Build the base query for latest prices with optional filters.

    Returns (columns_query, count_subquery_conditions) that share the same
    WHERE clauses for consistency.
    """
    latest_date_subquery = select(func.max(DailyPrice.date)).scalar_subquery()

    conditions = [DailyPrice.date == latest_date_subquery]

    if search:
        conditions.append(Commodity.name.ilike(f"%{search}%"))
    if category:
        conditions.append(Commodity.category == category)
    if region_id is not None:
        conditions.append(DailyPrice.region_id == region_id)

    return conditions, latest_date_subquery


async def get_latest_prices(
    session: AsyncSession,
    *,
    search: str | None = None,
    category: str | None = None,
    region_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[dict], int]:
    """Return (items, total_count) for latest prices with server-side filtering."""
    conditions, _ = _build_latest_base_query(
        search=search, category=category, region_id=region_id
    )

    base = (
        select(
            DailyPrice.commodity_id,
            Commodity.name.label("commodity_name"),
            Commodity.category.label("commodity_category"),
            DailyPrice.region_id,
            Region.code.label("region_code"),
            DailyPrice.date,
            func.avg(DailyPrice.price_prevailing).label("avg_price"),
        )
        .join(Commodity, Commodity.id == DailyPrice.commodity_id)
        .join(Region, Region.id == DailyPrice.region_id)
        .where(*conditions)
        .group_by(
            DailyPrice.commodity_id,
            Commodity.name,
            Commodity.category,
            DailyPrice.region_id,
            Region.code,
            DailyPrice.date,
        )
    )

    # Count total matching groups
    count_stmt = select(func.count()).select_from(base.subquery())
    total = await session.scalar(count_stmt) or 0

    # Fetch the page
    page_stmt = base.order_by(Commodity.name.asc(), Region.code.asc()).limit(limit).offset(offset)
    result = await session.execute(page_stmt)
    items = [dict(row._mapping) for row in result]

    return items, total


async def get_price_history(
    session: AsyncSession,
    *,
    commodity_id: int,
    region_id: int | None,
    from_date: date | None,
    to_date: date | None,
) -> list[dict]:
    statement = select(
        DailyPrice.date,
        func.avg(DailyPrice.price_prevailing).label("avg_price"),
    ).where(DailyPrice.commodity_id == commodity_id)

    if region_id is not None:
        statement = statement.where(DailyPrice.region_id == region_id)
    if from_date is not None:
        statement = statement.where(DailyPrice.date >= from_date)
    if to_date is not None:
        statement = statement.where(DailyPrice.date <= to_date)

    statement = statement.group_by(DailyPrice.date).order_by(DailyPrice.date.asc())

    result = await session.execute(statement)
    return [dict(row._mapping) for row in result]
