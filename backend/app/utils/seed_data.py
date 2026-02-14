from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Commodity, Market, Region

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

    await session.commit()
