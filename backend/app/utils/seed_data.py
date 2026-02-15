from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Commodity, DailyPrice, Market, Region

SEED_REGIONS = [
    {"name": "National Capital Region", "code": "NCR", "island_group": "Luzon"},
    {"name": "Bicol", "code": "R05", "island_group": "Luzon"},
    {"name": "Central Visayas", "code": "R07", "island_group": "Visayas"},
]

SEED_COMMODITIES = [
    {"name": "Well-Milled Rice", "category": "Rice", "unit": "kg", "image_url": None},
    {"name": "Red Onion", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Pork Liempo", "category": "Meat", "unit": "kg", "image_url": None},
]

SEED_MARKETS = [
    {"name": "Commonwealth Market", "region_code": "NCR", "type": "wet", "address": "Quezon City"},
    {"name": "Naga City Public Market", "region_code": "R05", "type": "wet", "address": "Naga City"},
    {"name": "Carbon Public Market", "region_code": "R07", "type": "wet", "address": "Cebu City"},
]


async def seed_reference_data(session: AsyncSession) -> None:
    region_count = await session.scalar(select(func.count(Region.id)))
    if region_count == 0:
        session.add_all([Region(**region) for region in SEED_REGIONS])
        await session.flush()

    commodity_count = await session.scalar(select(func.count(Commodity.id)))
    if commodity_count == 0:
        session.add_all([Commodity(**commodity) for commodity in SEED_COMMODITIES])

    market_count = await session.scalar(select(func.count(Market.id)))
    if market_count == 0:
        region_rows = await session.execute(select(Region))
        region_by_code = {region.code: region.id for region in region_rows.scalars().all()}
        market_records = [
            Market(
                name=market["name"],
                region_id=region_by_code[market["region_code"]],
                type=market["type"],
                address=market["address"],
            )
            for market in SEED_MARKETS
            if market["region_code"] in region_by_code
        ]
        session.add_all(market_records)

    daily_price_count = await session.scalar(select(func.count(DailyPrice.id)))
    if daily_price_count == 0:
        commodity_rows = await session.execute(select(Commodity))
        commodities = {row.name: row for row in commodity_rows.scalars().all()}

        region_rows = await session.execute(select(Region))
        regions = {row.id: row for row in region_rows.scalars().all()}

        market_rows = await session.execute(select(Market))
        markets = list(market_rows.scalars().all())

        base_price_by_commodity = {
            "Well-Milled Rice": Decimal("48.00"),
            "Red Onion": Decimal("130.00"),
            "Pork Liempo": Decimal("325.00"),
        }

        region_adjustment = {
            "NCR": Decimal("4.50"),
            "R05": Decimal("-2.00"),
            "R07": Decimal("1.50"),
        }

        start_date = datetime.now(UTC).date() - timedelta(days=83)
        records_to_add: list[DailyPrice] = []

        for market in markets:
            region = regions.get(market.region_id)
            if region is None:
                continue

            for commodity_name, base_price in base_price_by_commodity.items():
                commodity = commodities.get(commodity_name)
                if commodity is None:
                    continue

                adjustment = region_adjustment.get(region.code, Decimal("0.00"))

                for day_offset in range(84):
                    current_date = start_date + timedelta(days=day_offset)
                    trend = Decimal(str(day_offset)) * Decimal("0.12")
                    weekly_wave = Decimal(str((day_offset % 7) - 3)) * Decimal("0.35")
                    prevailing = (base_price + adjustment + trend + weekly_wave).quantize(Decimal("0.01"))

                    records_to_add.append(
                        DailyPrice(
                            commodity_id=commodity.id,
                            market_id=market.id,
                            region_id=region.id,
                            price_low=(prevailing - Decimal("2.00")).quantize(Decimal("0.01")),
                            price_high=(prevailing + Decimal("2.00")).quantize(Decimal("0.01")),
                            price_avg=prevailing,
                            price_prevailing=prevailing,
                            date=current_date,
                            source="SEED",
                        )
                    )

        session.add_all(records_to_add)

    await session.commit()
