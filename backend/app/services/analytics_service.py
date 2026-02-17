from datetime import date

from sqlalchemy import Date, Float, Integer, and_, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Commodity, DailyPrice, Region


async def get_weekly_variance(session: AsyncSession) -> list[dict]:
    week_start_expr = cast(func.date_trunc("week", DailyPrice.date), Date)

    weekly_base = (
        select(
            week_start_expr.label("week_start"),
            DailyPrice.commodity_id.label("commodity_id"),
            Commodity.name.label("commodity_name"),
            func.avg(DailyPrice.price_prevailing).label("weekly_avg_price"),
        )
        .join(Commodity, Commodity.id == DailyPrice.commodity_id)
        .group_by(week_start_expr, DailyPrice.commodity_id, Commodity.name)
        .subquery()
    )

    lag_value = func.lag(weekly_base.c.weekly_avg_price).over(
        partition_by=weekly_base.c.commodity_id,
        order_by=weekly_base.c.week_start,
    )

    wow_percent = cast(
        ((weekly_base.c.weekly_avg_price - lag_value) / func.nullif(lag_value, 0)) * 100,
        Float,
    ).label("wow_percent_change")

    statement = select(
        weekly_base.c.week_start,
        weekly_base.c.commodity_id,
        weekly_base.c.commodity_name,
        weekly_base.c.weekly_avg_price,
        wow_percent,
    ).order_by(weekly_base.c.week_start.desc(), weekly_base.c.commodity_name.asc())

    result = await session.execute(statement)
    return [dict(row._mapping) for row in result]


async def get_regional_comparison(
    session: AsyncSession,
    *,
    commodity_id: int | None,
    from_date: date | None,
    to_date: date | None,
) -> list[dict]:
    statement = select(
        Region.id.label("region_id"),
        Region.name.label("region_name"),
        Region.code.label("region_code"),
        func.avg(DailyPrice.price_prevailing).label("avg_price"),
    ).join(Region, Region.id == DailyPrice.region_id)

    if commodity_id is not None:
        statement = statement.where(DailyPrice.commodity_id == commodity_id)
    if from_date is not None:
        statement = statement.where(DailyPrice.date >= from_date)
    if to_date is not None:
        statement = statement.where(DailyPrice.date <= to_date)

    statement = statement.group_by(Region.id, Region.name, Region.code).order_by(
        func.avg(DailyPrice.price_prevailing).asc()
    )

    result = await session.execute(statement)
    return [dict(row._mapping) for row in result]


async def get_price_spikes(
    session: AsyncSession,
    *,
    commodity_id: int | None,
    region_id: int | None,
) -> list[dict]:
    rolling_base = select(
        DailyPrice.commodity_id,
        DailyPrice.region_id,
        DailyPrice.date,
        DailyPrice.price_prevailing.label("avg_price"),
        cast(
            func.avg(DailyPrice.price_prevailing).over(
                partition_by=(DailyPrice.commodity_id, DailyPrice.region_id),
                order_by=DailyPrice.date,
                rows=(-29, 0),
            ),
            Float,
        ).label("rolling_mean_30"),
        cast(
            func.stddev_samp(DailyPrice.price_prevailing).over(
                partition_by=(DailyPrice.commodity_id, DailyPrice.region_id),
                order_by=DailyPrice.date,
                rows=(-29, 0),
            ),
            Float,
        ).label("rolling_std_30"),
    )

    if commodity_id is not None:
        rolling_base = rolling_base.where(DailyPrice.commodity_id == commodity_id)
    if region_id is not None:
        rolling_base = rolling_base.where(DailyPrice.region_id == region_id)

    rolling_subquery = rolling_base.subquery()

    statement = (
        select(
            rolling_subquery.c.commodity_id,
            rolling_subquery.c.region_id,
            rolling_subquery.c.date,
            rolling_subquery.c.avg_price,
            rolling_subquery.c.rolling_mean_30,
            rolling_subquery.c.rolling_std_30,
        )
        .where(
            and_(
                rolling_subquery.c.rolling_std_30.is_not(None),
                func.abs(rolling_subquery.c.avg_price - rolling_subquery.c.rolling_mean_30)
                > (2 * rolling_subquery.c.rolling_std_30),
            )
        )
        .order_by(rolling_subquery.c.date.desc())
        .limit(200)
    )

    result = await session.execute(statement)
    return [dict(row._mapping) for row in result]


async def get_cheapest_region(session: AsyncSession, *, commodity_id: int) -> dict | None:
    latest_date_subquery = (
        select(func.max(DailyPrice.date)).where(DailyPrice.commodity_id == commodity_id).scalar_subquery()
    )

    statement = (
        select(
            Commodity.id.label("commodity_id"),
            Commodity.name.label("commodity_name"),
            Region.id.label("region_id"),
            Region.name.label("region_name"),
            Region.code.label("region_code"),
            func.avg(DailyPrice.price_prevailing).label("avg_price"),
            DailyPrice.date,
        )
        .join(Commodity, Commodity.id == DailyPrice.commodity_id)
        .join(Region, Region.id == DailyPrice.region_id)
        .where(and_(DailyPrice.commodity_id == commodity_id, DailyPrice.date == latest_date_subquery))
        .group_by(Commodity.id, Commodity.name, Region.id, Region.name, Region.code, DailyPrice.date)
        .order_by(func.avg(DailyPrice.price_prevailing).asc())
        .limit(1)
    )

    result = await session.execute(statement)
    row = result.first()
    return dict(row._mapping) if row else None


async def get_rolling_average(session: AsyncSession, *, commodity_id: int, region_id: int | None) -> list[dict]:
    statement = select(
        DailyPrice.date,
        DailyPrice.price_prevailing.label("avg_price"),
        cast(
            func.avg(DailyPrice.price_prevailing).over(
                partition_by=DailyPrice.region_id,
                order_by=DailyPrice.date,
                rows=(-29, 0),
            ),
            Float,
        ).label("rolling_30_day_avg"),
    ).where(DailyPrice.commodity_id == commodity_id)

    if region_id is not None:
        statement = statement.where(DailyPrice.region_id == region_id)

    statement = statement.order_by(DailyPrice.date.asc())

    result = await session.execute(statement)
    return [dict(row._mapping) for row in result]


async def get_seasonal_pattern(session: AsyncSession, *, commodity_id: int) -> list[dict]:
    month_expr = cast(func.extract("month", DailyPrice.date), Integer)

    statement = (
        select(
            month_expr.label("month"),
            func.avg(DailyPrice.price_prevailing).label("avg_price"),
        )
        .where(DailyPrice.commodity_id == commodity_id)
        .group_by(month_expr)
        .order_by(month_expr.asc())
    )

    result = await session.execute(statement)
    rows = []
    for row in result:
        mapped = dict(row._mapping)
        mapped["month"] = int(mapped["month"])
        rows.append(mapped)

    return rows
