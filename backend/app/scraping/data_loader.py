from decimal import Decimal

from sqlalchemy import Select, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Commodity, DailyPrice, Market, Region
from app.scraping.types import RawPriceRecord


async def _lookup_ids(session: AsyncSession, query: Select[tuple]) -> dict[str, int]:
    result = await session.execute(query)
    return {key: identifier for key, identifier in result.all()}


async def upsert_daily_prices(session: AsyncSession, records: list[RawPriceRecord]) -> int:
    if not records:
        return 0

    commodity_ids = await _lookup_ids(session, select(Commodity.name, Commodity.id))
    region_ids = await _lookup_ids(session, select(Region.code, Region.id))
    market_ids = await _lookup_ids(session, select(Market.name, Market.id))

    rows_to_insert: list[dict] = []

    for record in records:
        commodity_id = commodity_ids.get(record.commodity_name)
        region_id = region_ids.get(record.region_code)
        market_id = market_ids.get(record.market_name)

        if not (commodity_id and region_id and market_id):
            continue

        prevailing = Decimal(str(record.price_prevailing))
        low = Decimal(str(record.price_low)) if record.price_low is not None else None
        high = Decimal(str(record.price_high)) if record.price_high is not None else None

        rows_to_insert.append(
            {
                "commodity_id": commodity_id,
                "market_id": market_id,
                "region_id": region_id,
                "price_prevailing": prevailing,
                "price_low": low,
                "price_high": high,
                "price_avg": prevailing,
                "date": record.date,
                "source": record.source,
            }
        )

    if not rows_to_insert:
        return 0

    statement = insert(DailyPrice).values(rows_to_insert)
    upsert_statement = statement.on_conflict_do_update(
        constraint="uq_daily_prices_commodity_market_date_source",
        set_={
            "price_low": statement.excluded.price_low,
            "price_high": statement.excluded.price_high,
            "price_avg": statement.excluded.price_avg,
            "price_prevailing": statement.excluded.price_prevailing,
        },
    )

    await session.execute(upsert_statement)
    await session.commit()

    return len(rows_to_insert)
