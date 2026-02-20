"""Seed data for Agri-Senta: Lagonoy Municipal Agriculture Office.

Lagonoy is a coastal municipality in Camarines Sur (Bicol Region) facing
Lagonoy Gulf.  This seeds barangays as "regions", local commodities,
local markets, and 90 days of realistic daily price history.
"""

import hashlib
import math
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Commodity, DailyPrice, Market, Region

# ---------------------------------------------------------------------------
# Barangays of Lagonoy, Camarines Sur  (stored in the Region table)
#   code  → short barangay code
#   island_group → repurposed as "zone" (Poblacion / Coastal / Upland / Agricultural)
# ---------------------------------------------------------------------------
SEED_REGIONS = [
    {"name": "Barangay 1 (Poblacion)", "code": "POB1", "island_group": "Poblacion"},
    {"name": "Barangay 2 (Poblacion)", "code": "POB2", "island_group": "Poblacion"},
    {"name": "Barangay 3 (Poblacion)", "code": "POB3", "island_group": "Poblacion"},
    {"name": "Barangay 4 (Poblacion)", "code": "POB4", "island_group": "Poblacion"},
    {"name": "Barangay 5 (Poblacion)", "code": "POB5", "island_group": "Poblacion"},
    {"name": "Awayan", "code": "AWA", "island_group": "Agricultural"},
    {"name": "Baliuag Nuevo", "code": "BLN", "island_group": "Agricultural"},
    {"name": "Baliuag Viejo", "code": "BLV", "island_group": "Agricultural"},
    {"name": "Binanuahan", "code": "BIN", "island_group": "Coastal"},
    {"name": "Bocogan", "code": "BOC", "island_group": "Upland"},
    {"name": "Caigdal", "code": "CGD", "island_group": "Agricultural"},
    {"name": "Damulog", "code": "DAM", "island_group": "Upland"},
    {"name": "Gabi", "code": "GAB", "island_group": "Agricultural"},
    {"name": "Gabusan", "code": "GBS", "island_group": "Agricultural"},
    {"name": "Himanag", "code": "HMN", "island_group": "Coastal"},
    {"name": "Langka", "code": "LNK", "island_group": "Agricultural"},
    {"name": "Loho", "code": "LOH", "island_group": "Upland"},
    {"name": "Manguiring", "code": "MNG", "island_group": "Coastal"},
    {"name": "Olas", "code": "OLS", "island_group": "Coastal"},
    {"name": "Omalo", "code": "OMA", "island_group": "Agricultural"},
    {"name": "Panagan", "code": "PAN", "island_group": "Agricultural"},
    {"name": "Panicuan", "code": "PNC", "island_group": "Agricultural"},
    {"name": "San Francisco", "code": "SFC", "island_group": "Upland"},
    {"name": "San Isidro", "code": "SIS", "island_group": "Agricultural"},
    {"name": "San Rafael", "code": "SRF", "island_group": "Agricultural"},
    {"name": "Santa Cruz", "code": "SCZ", "island_group": "Upland"},
    {"name": "Sipaco", "code": "SPC", "island_group": "Coastal"},
    {"name": "Sipi", "code": "SPI", "island_group": "Agricultural"},
    {"name": "Tagas", "code": "TGS", "island_group": "Upland"},
    {"name": "Tamban", "code": "TMB", "island_group": "Coastal"},
]

# ---------------------------------------------------------------------------
# ~87 locally relevant commodities for Lagonoy, Camarines Sur
#   Focus: Bicol staples, coconut products, Lagonoy Gulf seafood, local vegs
#   (name, category, unit, base_price_php)
# ---------------------------------------------------------------------------
_RAW_COMMODITIES: list[tuple[str, str, str, float]] = [
    # ── Rice & Grains (10) ──
    ("Well-Milled Rice", "Rice & Grains", "kg", 48),
    ("Regular-Milled Rice", "Rice & Grains", "kg", 42),
    ("Premium Rice", "Rice & Grains", "kg", 56),
    ("NFA Rice", "Rice & Grains", "kg", 38),
    ("Glutinous Rice (Malagkit)", "Rice & Grains", "kg", 55),
    ("Sinandomeng Rice", "Rice & Grains", "kg", 52),
    ("Dinorado Rice", "Rice & Grains", "kg", 60),
    ("Corn Grits", "Rice & Grains", "kg", 35),
    ("Mongo (Mung Bean)", "Rice & Grains", "kg", 90),
    ("Peanut (Mani)", "Rice & Grains", "kg", 110),

    # ── Vegetables (20) ──
    ("Tomato", "Vegetables", "kg", 60),
    ("Red Onion", "Vegetables", "kg", 130),
    ("Garlic (Local)", "Vegetables", "kg", 200),
    ("Eggplant (Talong)", "Vegetables", "kg", 55),
    ("Ampalaya (Bitter Gourd)", "Vegetables", "kg", 80),
    ("Squash (Kalabasa)", "Vegetables", "kg", 35),
    ("Kangkong (Water Spinach)", "Vegetables", "kg", 30),
    ("Sitaw (String Beans)", "Vegetables", "kg", 70),
    ("Chili Labuyo (Siling Labuyo)", "Vegetables", "kg", 250),
    ("Chili Siling Haba", "Vegetables", "kg", 120),
    ("Ginger (Luya)", "Vegetables", "kg", 120),
    ("Pechay (Bok Choy)", "Vegetables", "kg", 40),
    ("Sayote (Chayote)", "Vegetables", "kg", 35),
    ("Okra", "Vegetables", "kg", 65),
    ("Malunggay (Moringa)", "Vegetables", "kg", 60),
    ("Sweet Potato (Kamote)", "Vegetables", "kg", 40),
    ("Gabi (Taro)", "Vegetables", "kg", 45),
    ("Puso ng Saging (Banana Heart)", "Vegetables", "kg", 45),
    ("Saluyot (Jute Leaves)", "Vegetables", "kg", 55),
    ("Alugbati (Malabar Spinach)", "Vegetables", "kg", 50),

    # ── Fish & Seafood — Lagonoy Gulf (18) ──
    ("Galunggong (Round Scad)", "Fish & Seafood", "kg", 160),
    ("Tulingan (Skipjack Tuna)", "Fish & Seafood", "kg", 200),
    ("Tambakol (Yellowfin Tuna)", "Fish & Seafood", "kg", 250),
    ("Bangus (Milkfish)", "Fish & Seafood", "kg", 170),
    ("Tilapia", "Fish & Seafood", "kg", 120),
    ("Lapu-Lapu (Grouper)", "Fish & Seafood", "kg", 400),
    ("Maya-Maya (Red Snapper)", "Fish & Seafood", "kg", 350),
    ("Hipon (Shrimp)", "Fish & Seafood", "kg", 280),
    ("Pusit (Squid)", "Fish & Seafood", "kg", 260),
    ("Alimasag (Blue Crab)", "Fish & Seafood", "kg", 280),
    ("Tahong (Green Mussel)", "Fish & Seafood", "kg", 120),
    ("Talaba (Oyster)", "Fish & Seafood", "kg", 150),
    ("Dilis (Anchovies)", "Fish & Seafood", "kg", 180),
    ("Hasa-Hasa (Short Mackerel)", "Fish & Seafood", "kg", 140),
    ("Tanigue (Spanish Mackerel)", "Fish & Seafood", "kg", 380),
    ("Tuyo (Dried Herring)", "Fish & Seafood", "kg", 200),
    ("Tinapa (Smoked Fish)", "Fish & Seafood", "kg", 180),
    ("Dried Dilis", "Fish & Seafood", "kg", 250),

    # ── Meat (10) ──
    ("Pork Liempo", "Meat", "kg", 325),
    ("Pork Kasim", "Meat", "kg", 280),
    ("Pork Pata", "Meat", "kg", 230),
    ("Ground Pork", "Meat", "kg", 270),
    ("Whole Chicken", "Meat", "kg", 190),
    ("Chicken Breast", "Meat", "kg", 210),
    ("Chicken Thigh", "Meat", "kg", 185),
    ("Beef Brisket", "Meat", "kg", 380),
    ("Beef Shank (Bulalo)", "Meat", "kg", 360),
    ("Goat Meat (Chevon)", "Meat", "kg", 400),

    # ── Fruits (10) ──
    ("Banana (Saba/Cooking)", "Fruits", "kg", 55),
    ("Banana (Lakatan)", "Fruits", "kg", 65),
    ("Calamansi", "Fruits", "kg", 80),
    ("Papaya", "Fruits", "kg", 45),
    ("Coconut (Buko)", "Fruits", "pc", 40),
    ("Pineapple", "Fruits", "kg", 50),
    ("Mango (Carabao)", "Fruits", "kg", 100),
    ("Jackfruit (Langka)", "Fruits", "kg", 70),
    ("Watermelon", "Fruits", "kg", 35),
    ("Avocado", "Fruits", "kg", 100),

    # ── Coconut Products — Bicol specialty (6) ──
    ("Copra", "Coconut Products", "kg", 38),
    ("Coconut Oil (Virgin)", "Coconut Products", "L", 180),
    ("Coconut Milk (Gata)", "Coconut Products", "L", 80),
    ("Coconut Cream", "Coconut Products", "L", 110),
    ("Desiccated Coconut", "Coconut Products", "kg", 160),
    ("Coco Sugar", "Coconut Products", "kg", 200),

    # ── Eggs & Dairy (5) ──
    ("Egg (Large)", "Eggs & Dairy", "pc", 8),
    ("Egg (Medium)", "Eggs & Dairy", "pc", 7),
    ("Salted Egg (Itlog na Maalat)", "Eggs & Dairy", "pc", 12),
    ("Evaporated Milk", "Eggs & Dairy", "can", 38),
    ("Condensed Milk", "Eggs & Dairy", "can", 42),

    # ── Spices & Condiments (8) ──
    ("Salt (Iodized)", "Spices & Condiments", "kg", 25),
    ("Soy Sauce", "Spices & Condiments", "bottle", 30),
    ("Vinegar (Coconut)", "Spices & Condiments", "bottle", 35),
    ("Fish Sauce (Patis)", "Spices & Condiments", "bottle", 30),
    ("Bagoong (Shrimp Paste)", "Spices & Condiments", "bottle", 80),
    ("Cooking Oil (Coconut)", "Spices & Condiments", "L", 85),
    ("Cooking Oil (Palm)", "Spices & Condiments", "L", 72),
    ("Banana Ketchup", "Spices & Condiments", "bottle", 35),
]

# Derived structures -------------------------------------------------------
SEED_COMMODITIES = [
    {"name": name, "category": cat, "unit": unit, "image_url": None}
    for name, cat, unit, _ in _RAW_COMMODITIES
]

BASE_PRICES: dict[str, Decimal] = {
    name: Decimal(str(price)) for name, _, _, price in _RAW_COMMODITIES
}

# ---------------------------------------------------------------------------
# Markets in Lagonoy  (primary public market + satellite buying stations)
# ---------------------------------------------------------------------------
SEED_MARKETS = [
    {"name": "Lagonoy Public Market", "region_code": "POB1", "type": "wet", "address": "Poblacion, Lagonoy, Camarines Sur"},
    {"name": "Lagonoy Dry Goods Market", "region_code": "POB2", "type": "dry", "address": "Poblacion, Lagonoy, Camarines Sur"},
    {"name": "Binanuahan Fish Landing", "region_code": "BIN", "type": "fish_port", "address": "Binanuahan, Lagonoy, Camarines Sur"},
    {"name": "Himanag Coastal Market", "region_code": "HMN", "type": "wet", "address": "Himanag, Lagonoy, Camarines Sur"},
    {"name": "San Isidro Buying Station", "region_code": "SIS", "type": "buying_station", "address": "San Isidro, Lagonoy, Camarines Sur"},
]

# ---------------------------------------------------------------------------
# Volatility & spread multipliers per category
# ---------------------------------------------------------------------------
_CATEGORY_VOLATILITY: dict[str, float] = {
    "Rice & Grains": 0.006,
    "Vegetables": 0.025,
    "Fish & Seafood": 0.022,
    "Meat": 0.008,
    "Fruits": 0.018,
    "Coconut Products": 0.015,
    "Eggs & Dairy": 0.010,
    "Spices & Condiments": 0.007,
}

_CATEGORY_SPREAD: dict[str, Decimal] = {
    "Rice & Grains": Decimal("0.04"),
    "Vegetables": Decimal("0.08"),
    "Fish & Seafood": Decimal("0.07"),
    "Meat": Decimal("0.03"),
    "Fruits": Decimal("0.07"),
    "Coconut Products": Decimal("0.05"),
    "Eggs & Dairy": Decimal("0.04"),
    "Spices & Condiments": Decimal("0.03"),
}

# Barangay zone price adjustments
_REGION_PCT: dict[str, float] = {
    "POB1": 0.03, "POB2": 0.03, "POB3": 0.02, "POB4": 0.02, "POB5": 0.01,
    "AWA": -0.02, "BLN": -0.03, "BLV": -0.03,
    "BIN": -0.01, "BOC": -0.04,
    "CGD": -0.02, "DAM": -0.04,
    "GAB": -0.02, "GBS": -0.03,
    "HMN": 0.00, "LNK": -0.02,
    "LOH": -0.04, "MNG": -0.01,
    "OLS": -0.01, "OMA": -0.03,
    "PAN": -0.02, "PNC": -0.02,
    "SFC": -0.04, "SIS": -0.01,
    "SRF": -0.02, "SCZ": -0.03,
    "SPC": 0.00, "SPI": -0.02,
    "TGS": -0.03, "TMB": -0.01,
}

HISTORY_DAYS = 90


def _deterministic_noise(seed_str: str, day: int) -> float:
    """Return a deterministic float in [-1, 1] for reproducible price curves."""
    raw = hashlib.md5(f"{seed_str}:{day}".encode()).hexdigest()  # noqa: S324
    return (int(raw[:8], 16) / 0xFFFFFFFF) * 2 - 1


async def seed_reference_data(session: AsyncSession) -> None:
    # ------------------------------------------------------------------
    # 1. Barangays (stored in regions table)
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
    # 3. Markets
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

                cat = commodity.category
                volatility = _CATEGORY_VOLATILITY.get(cat, 0.01)
                spread_pct = _CATEGORY_SPREAD.get(cat, Decimal("0.05"))
                regional_base = base_price * (1 + Decimal(str(region_pct)))
                pair_seed = f"{region.code}:{commodity_name}"

                for day_offset in range(HISTORY_DAYS):
                    current_date = start_date + timedelta(days=day_offset)
                    trend_factor = Decimal(str(1 + day_offset * 0.0004))
                    weekday = current_date.weekday()
                    weekly_wave = Decimal(str(math.sin(2 * math.pi * weekday / 7) * volatility * 1.5))
                    noise_val = _deterministic_noise(pair_seed, day_offset)
                    noise = Decimal(str(noise_val * volatility))

                    prevailing = (regional_base * trend_factor * (1 + weekly_wave + noise)).quantize(Decimal("0.01"))
                    if prevailing < Decimal("1.00"):
                        prevailing = Decimal("1.00")

                    half_spread = (prevailing * spread_pct / 2).quantize(Decimal("0.01"))

                    records.append(
                        DailyPrice(
                            commodity_id=commodity.id,
                            market_id=market.id,
                            region_id=region.id,
                            price_low=prevailing - half_spread,
                            price_high=prevailing + half_spread,
                            price_avg=prevailing,
                            price_prevailing=prevailing,
                            date=current_date,
                            source="MAO-Lagonoy",
                        )
                    )

        batch_size = 10000
        for i in range(0, len(records), batch_size):
            session.add_all(records[i : i + batch_size])
            await session.flush()

    await session.commit()
