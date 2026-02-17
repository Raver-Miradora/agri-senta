"""Seed data for Agri-Senta: all 17 Philippine regions, 35 commodities, 17 markets.

Generates 90 days of realistic daily price history for every
commodity-region pair with category-specific volatility, seasonal
patterns, and regional price differentials.
"""

import hashlib
import math
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Commodity, DailyPrice, Market, Region

# ---------------------------------------------------------------------------
# All 17 Philippine administrative regions
# ---------------------------------------------------------------------------
SEED_REGIONS = [
    {"name": "National Capital Region", "code": "NCR", "island_group": "Luzon"},
    {"name": "Cordillera Administrative Region", "code": "CAR", "island_group": "Luzon"},
    {"name": "Ilocos Region", "code": "R01", "island_group": "Luzon"},
    {"name": "Cagayan Valley", "code": "R02", "island_group": "Luzon"},
    {"name": "Central Luzon", "code": "R03", "island_group": "Luzon"},
    {"name": "CALABARZON", "code": "R04A", "island_group": "Luzon"},
    {"name": "MIMAROPA", "code": "R04B", "island_group": "Luzon"},
    {"name": "Bicol Region", "code": "R05", "island_group": "Luzon"},
    {"name": "Western Visayas", "code": "R06", "island_group": "Visayas"},
    {"name": "Central Visayas", "code": "R07", "island_group": "Visayas"},
    {"name": "Eastern Visayas", "code": "R08", "island_group": "Visayas"},
    {"name": "Zamboanga Peninsula", "code": "R09", "island_group": "Mindanao"},
    {"name": "Northern Mindanao", "code": "R10", "island_group": "Mindanao"},
    {"name": "Davao Region", "code": "R11", "island_group": "Mindanao"},
    {"name": "SOCCSKSARGEN", "code": "R12", "island_group": "Mindanao"},
    {"name": "Caraga", "code": "R13", "island_group": "Mindanao"},
    {"name": "Bangsamoro", "code": "BARMM", "island_group": "Mindanao"},
]

# ---------------------------------------------------------------------------
# 35 key Philippine commodities across 8 categories
# Prices sourced from typical DA / Bantay Presyo ranges
# ---------------------------------------------------------------------------
SEED_COMMODITIES = [
    # Rice
    {"name": "Well-Milled Rice", "category": "Rice", "unit": "kg", "image_url": None},
    {"name": "Regular-Milled Rice", "category": "Rice", "unit": "kg", "image_url": None},
    {"name": "Premium Rice", "category": "Rice", "unit": "kg", "image_url": None},
    {"name": "Special Rice", "category": "Rice", "unit": "kg", "image_url": None},
    # Vegetables
    {"name": "Red Onion", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "White Onion", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Garlic (Imported)", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Garlic (Local)", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Tomato", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Eggplant", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Ampalaya", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Squash", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Cabbage", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Kangkong", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Sitaw", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Chili (Labuyo)", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Ginger", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Potato", "category": "Vegetables", "unit": "kg", "image_url": None},
    {"name": "Carrots", "category": "Vegetables", "unit": "kg", "image_url": None},
    # Meat
    {"name": "Pork Liempo", "category": "Meat", "unit": "kg", "image_url": None},
    {"name": "Pork Kasim", "category": "Meat", "unit": "kg", "image_url": None},
    {"name": "Whole Chicken", "category": "Meat", "unit": "kg", "image_url": None},
    {"name": "Chicken Breast", "category": "Meat", "unit": "kg", "image_url": None},
    {"name": "Beef Brisket", "category": "Meat", "unit": "kg", "image_url": None},
    {"name": "Beef Rump", "category": "Meat", "unit": "kg", "image_url": None},
    # Fish & Seafood
    {"name": "Bangus", "category": "Fish & Seafood", "unit": "kg", "image_url": None},
    {"name": "Tilapia", "category": "Fish & Seafood", "unit": "kg", "image_url": None},
    {"name": "Galunggong", "category": "Fish & Seafood", "unit": "kg", "image_url": None},
    {"name": "Alumahan", "category": "Fish & Seafood", "unit": "kg", "image_url": None},
    {"name": "Shrimp (Suahe)", "category": "Fish & Seafood", "unit": "kg", "image_url": None},
    # Fruits
    {"name": "Banana (Lakatan)", "category": "Fruits", "unit": "kg", "image_url": None},
    {"name": "Calamansi", "category": "Fruits", "unit": "kg", "image_url": None},
    {"name": "Mango (Carabao)", "category": "Fruits", "unit": "kg", "image_url": None},
    # Poultry & Dairy
    {"name": "Egg (Large)", "category": "Poultry & Dairy", "unit": "pc", "image_url": None},
    # Other Essentials
    {"name": "Refined Sugar", "category": "Other Essentials", "unit": "kg", "image_url": None},
    {"name": "Brown Sugar", "category": "Other Essentials", "unit": "kg", "image_url": None},
    {"name": "Cooking Oil (Palm)", "category": "Other Essentials", "unit": "L", "image_url": None},
]

# ---------------------------------------------------------------------------
# One representative public market per region
# ---------------------------------------------------------------------------
SEED_MARKETS = [
    {"name": "Commonwealth Market", "region_code": "NCR", "type": "wet", "address": "Quezon City"},
    {"name": "Baguio City Public Market", "region_code": "CAR", "type": "wet", "address": "Baguio City"},
    {"name": "Vigan Public Market", "region_code": "R01", "type": "wet", "address": "Vigan, Ilocos Sur"},
    {"name": "Tuguegarao Center Market", "region_code": "R02", "type": "wet", "address": "Tuguegarao, Cagayan"},
    {"name": "Pampanga Public Market", "region_code": "R03", "type": "wet", "address": "San Fernando, Pampanga"},
    {"name": "Lucena Grand Central Market", "region_code": "R04A", "type": "wet", "address": "Lucena City, Quezon"},
    {"name": "Puerto Princesa Main Market", "region_code": "R04B", "type": "wet", "address": "Puerto Princesa, Palawan"},
    {"name": "Naga City Public Market", "region_code": "R05", "type": "wet", "address": "Naga City, Camarines Sur"},
    {"name": "Iloilo Terminal Market", "region_code": "R06", "type": "wet", "address": "Iloilo City"},
    {"name": "Carbon Public Market", "region_code": "R07", "type": "wet", "address": "Cebu City"},
    {"name": "Tacloban Public Market", "region_code": "R08", "type": "wet", "address": "Tacloban City, Leyte"},
    {"name": "Zamboanga City Central Market", "region_code": "R09", "type": "wet", "address": "Zamboanga City"},
    {"name": "Cogon Market", "region_code": "R10", "type": "wet", "address": "Cagayan de Oro, Misamis Oriental"},
    {"name": "Bankerohan Public Market", "region_code": "R11", "type": "wet", "address": "Davao City"},
    {"name": "General Santos Public Market", "region_code": "R12", "type": "wet", "address": "General Santos City"},
    {"name": "Butuan City Central Market", "region_code": "R13", "type": "wet", "address": "Butuan City, Agusan del Norte"},
    {"name": "Cotabato City Public Market", "region_code": "BARMM", "type": "wet", "address": "Cotabato City"},
]

# ---------------------------------------------------------------------------
# Base prevailing prices (PHP) and category-level volatility controls
# ---------------------------------------------------------------------------
BASE_PRICES: dict[str, Decimal] = {
    # Rice
    "Well-Milled Rice": Decimal("48.00"),
    "Regular-Milled Rice": Decimal("42.00"),
    "Premium Rice": Decimal("56.00"),
    "Special Rice": Decimal("62.00"),
    # Vegetables
    "Red Onion": Decimal("130.00"),
    "White Onion": Decimal("110.00"),
    "Garlic (Imported)": Decimal("140.00"),
    "Garlic (Local)": Decimal("200.00"),
    "Tomato": Decimal("60.00"),
    "Eggplant": Decimal("55.00"),
    "Ampalaya": Decimal("80.00"),
    "Squash": Decimal("35.00"),
    "Cabbage": Decimal("50.00"),
    "Kangkong": Decimal("30.00"),
    "Sitaw": Decimal("70.00"),
    "Chili (Labuyo)": Decimal("250.00"),
    "Ginger": Decimal("120.00"),
    "Potato": Decimal("85.00"),
    "Carrots": Decimal("90.00"),
    # Meat
    "Pork Liempo": Decimal("325.00"),
    "Pork Kasim": Decimal("280.00"),
    "Whole Chicken": Decimal("190.00"),
    "Chicken Breast": Decimal("210.00"),
    "Beef Brisket": Decimal("380.00"),
    "Beef Rump": Decimal("400.00"),
    # Fish & Seafood
    "Bangus": Decimal("170.00"),
    "Tilapia": Decimal("120.00"),
    "Galunggong": Decimal("160.00"),
    "Alumahan": Decimal("200.00"),
    "Shrimp (Suahe)": Decimal("350.00"),
    # Fruits
    "Banana (Lakatan)": Decimal("65.00"),
    "Calamansi": Decimal("80.00"),
    "Mango (Carabao)": Decimal("100.00"),
    # Poultry & Dairy
    "Egg (Large)": Decimal("8.00"),
    # Other Essentials
    "Refined Sugar": Decimal("75.00"),
    "Brown Sugar": Decimal("65.00"),
    "Cooking Oil (Palm)": Decimal("72.00"),
}

# Volatility & spread multipliers per category (higher = more day-to-day swing)
_CATEGORY_VOLATILITY: dict[str, float] = {
    "Rice": 0.006,
    "Vegetables": 0.025,
    "Meat": 0.008,
    "Fish & Seafood": 0.020,
    "Fruits": 0.018,
    "Poultry & Dairy": 0.010,
    "Other Essentials": 0.007,
}

# High-low spread as fraction of prevailing price per category
_CATEGORY_SPREAD: dict[str, Decimal] = {
    "Rice": Decimal("0.04"),
    "Vegetables": Decimal("0.08"),
    "Meat": Decimal("0.03"),
    "Fish & Seafood": Decimal("0.06"),
    "Fruits": Decimal("0.07"),
    "Poultry & Dairy": Decimal("0.04"),
    "Other Essentials": Decimal("0.03"),
}

# Regional price adjustments (percentage of base price)
# Positive = more expensive, negative = cheaper
_REGION_PCT: dict[str, float] = {
    "NCR": 0.06,
    "CAR": -0.02,
    "R01": -0.01,
    "R02": -0.04,
    "R03": 0.03,
    "R04A": 0.04,
    "R04B": 0.05,
    "R05": -0.02,
    "R06": -0.01,
    "R07": 0.01,
    "R08": -0.03,
    "R09": -0.02,
    "R10": 0.00,
    "R11": 0.01,
    "R12": -0.03,
    "R13": -0.04,
    "BARMM": -0.01,
}

HISTORY_DAYS = 90


def _deterministic_noise(seed_str: str, day: int) -> float:
    """Return a deterministic float in [-1, 1] for reproducible price curves.

    Uses an MD5 hash so the generated series is identical across restarts
    while still looking natural.
    """
    raw = hashlib.md5(f"{seed_str}:{day}".encode()).hexdigest()  # noqa: S324
    return (int(raw[:8], 16) / 0xFFFFFFFF) * 2 - 1


async def seed_reference_data(session: AsyncSession) -> None:
    # ------------------------------------------------------------------
    # 1. Regions
    # ------------------------------------------------------------------
    region_count = await session.scalar(select(func.count(Region.id)))
    if region_count == 0:
        session.add_all([Region(**r) for r in SEED_REGIONS])
        await session.flush()

    # ------------------------------------------------------------------
    # 2. Commodities
    # ------------------------------------------------------------------
    commodity_count = await session.scalar(select(func.count(Commodity.id)))
    if commodity_count == 0:
        session.add_all([Commodity(**c) for c in SEED_COMMODITIES])
        await session.flush()

    # ------------------------------------------------------------------
    # 3. Markets (one per region)
    # ------------------------------------------------------------------
    market_count = await session.scalar(select(func.count(Market.id)))
    if market_count == 0:
        region_rows = await session.execute(select(Region))
        region_by_code = {r.code: r.id for r in region_rows.scalars().all()}
        market_records = [
            Market(
                name=m["name"],
                region_id=region_by_code[m["region_code"]],
                type=m["type"],
                address=m["address"],
            )
            for m in SEED_MARKETS
            if m["region_code"] in region_by_code
        ]
        session.add_all(market_records)
        await session.flush()

    # ------------------------------------------------------------------
    # 4. Daily prices (HISTORY_DAYS per commodity-market pair)
    # ------------------------------------------------------------------
    daily_price_count = await session.scalar(select(func.count(DailyPrice.id)))
    if daily_price_count == 0:
        commodity_rows = await session.execute(select(Commodity))
        commodities = {row.name: row for row in commodity_rows.scalars().all()}

        region_rows = await session.execute(select(Region))
        regions = {row.id: row for row in region_rows.scalars().all()}

        market_rows = await session.execute(select(Market))
        markets = list(market_rows.scalars().all())

        start_date = datetime.now(UTC).date() - timedelta(days=HISTORY_DAYS - 1)
        records: list[DailyPrice] = []

        for market in markets:
            region = regions.get(market.region_id)
            if region is None:
                continue

            region_pct = _REGION_PCT.get(region.code, 0.0)

            for commodity_name, base_price in BASE_PRICES.items():
                commodity = commodities.get(commodity_name)
                if commodity is None:
                    continue

                # Lookup category properties
                cat = commodity.category
                volatility = _CATEGORY_VOLATILITY.get(cat, 0.01)
                spread_pct = _CATEGORY_SPREAD.get(cat, Decimal("0.05"))

                # Regional adjustment (absolute)
                regional_base = base_price * (1 + Decimal(str(region_pct)))

                # Deterministic seed for this pair
                pair_seed = f"{region.code}:{commodity_name}"

                for day_offset in range(HISTORY_DAYS):
                    current_date = start_date + timedelta(days=day_offset)

                    # Gentle upward trend (~0.04% per day ≈ 3.6% over 90 days)
                    trend_factor = Decimal(str(1 + day_offset * 0.0004))

                    # Weekly seasonality (weekend dip, midweek peak)
                    weekday = current_date.weekday()
                    weekly_wave = Decimal(str(math.sin(2 * math.pi * weekday / 7) * volatility * 1.5))

                    # Deterministic random noise
                    noise_val = _deterministic_noise(pair_seed, day_offset)
                    noise = Decimal(str(noise_val * volatility))

                    prevailing = (regional_base * trend_factor * (1 + weekly_wave + noise)).quantize(Decimal("0.01"))

                    # Ensure minimum price
                    if prevailing < Decimal("1.00"):
                        prevailing = Decimal("1.00")

                    half_spread = (prevailing * spread_pct / 2).quantize(Decimal("0.01"))
                    price_low = prevailing - half_spread
                    price_high = prevailing + half_spread
                    price_avg = prevailing

                    records.append(
                        DailyPrice(
                            commodity_id=commodity.id,
                            market_id=market.id,
                            region_id=region.id,
                            price_low=price_low,
                            price_high=price_high,
                            price_avg=price_avg,
                            price_prevailing=prevailing,
                            date=current_date,
                            source="DA-BPI",
                        )
                    )

        # Bulk-insert in batches to avoid memory pressure
        batch_size = 5000
        for i in range(0, len(records), batch_size):
            session.add_all(records[i : i + batch_size])
            await session.flush()

    await session.commit()
