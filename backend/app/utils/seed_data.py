from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Commodity, Region

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


async def seed_reference_data(session: AsyncSession) -> None:
    region_count = await session.scalar(select(func.count(Region.id)))
    if region_count == 0:
        session.add_all([Region(**region) for region in SEED_REGIONS])

    commodity_count = await session.scalar(select(func.count(Commodity.id)))
    if commodity_count == 0:
        session.add_all([Commodity(**commodity) for commodity in SEED_COMMODITIES])

    await session.commit()
