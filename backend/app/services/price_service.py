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


async def get_latest_prices(session: AsyncSession) -> list[dict]:
    latest_date_subquery = select(func.max(DailyPrice.date)).scalar_subquery()

    statement = (
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
        .where(DailyPrice.date == latest_date_subquery)
        .group_by(
            DailyPrice.commodity_id,
            Commodity.name,
            Commodity.category,
            DailyPrice.region_id,
            Region.code,
            DailyPrice.date,
        )
        .order_by(Commodity.name.asc(), Region.code.asc())
    )

    result = await session.execute(statement)
    return [dict(row._mapping) for row in result]


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
