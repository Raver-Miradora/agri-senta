"""Seed data for Agri-Senta: 17 Philippine regions, 210+ commodities, 17 markets.

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
# 222 key Philippine market commodities — compact tuple format:
#   (name, category, unit, base_price_php)
# Prices sourced from typical DA / Bantay Presyo ranges (PHP, 2024-2025)
# ---------------------------------------------------------------------------
_RAW_COMMODITIES: list[tuple[str, str, str, float]] = [
    # ── Rice (11) ──
    ("Well-Milled Rice", "Rice", "kg", 48),
    ("Regular-Milled Rice", "Rice", "kg", 42),
    ("Premium Rice", "Rice", "kg", 56),
    ("Special Rice", "Rice", "kg", 62),
    ("NFA Rice", "Rice", "kg", 38),
    ("Brown Rice", "Rice", "kg", 65),
    ("Glutinous Rice (Malagkit)", "Rice", "kg", 55),
    ("Jasmine Rice", "Rice", "kg", 58),
    ("Sinandomeng Rice", "Rice", "kg", 52),
    ("Dinorado Rice", "Rice", "kg", 60),
    ("Black Rice (Tapol)", "Rice", "kg", 85),

    # ── Vegetables (45) ──
    ("Red Onion", "Vegetables", "kg", 130),
    ("White Onion", "Vegetables", "kg", 110),
    ("Garlic (Imported)", "Vegetables", "kg", 140),
    ("Garlic (Local)", "Vegetables", "kg", 200),
    ("Tomato", "Vegetables", "kg", 60),
    ("Eggplant", "Vegetables", "kg", 55),
    ("Ampalaya (Bitter Gourd)", "Vegetables", "kg", 80),
    ("Squash (Kalabasa)", "Vegetables", "kg", 35),
    ("Cabbage", "Vegetables", "kg", 50),
    ("Kangkong (Water Spinach)", "Vegetables", "kg", 30),
    ("Sitaw (String Beans)", "Vegetables", "kg", 70),
    ("Chili (Labuyo)", "Vegetables", "kg", 250),
    ("Chili (Siling Haba)", "Vegetables", "kg", 120),
    ("Ginger (Luya)", "Vegetables", "kg", 120),
    ("Potato", "Vegetables", "kg", 85),
    ("Carrots", "Vegetables", "kg", 90),
    ("Pechay (Bok Choy)", "Vegetables", "kg", 40),
    ("Pechay Baguio (Wombok)", "Vegetables", "kg", 60),
    ("Sayote (Chayote)", "Vegetables", "kg", 35),
    ("Upo (Bottle Gourd)", "Vegetables", "kg", 30),
    ("Patola (Sponge Gourd)", "Vegetables", "kg", 45),
    ("Sweet Potato (Kamote)", "Vegetables", "kg", 40),
    ("Togue (Mung Bean Sprouts)", "Vegetables", "kg", 35),
    ("Malunggay (Moringa)", "Vegetables", "kg", 60),
    ("Okra", "Vegetables", "kg", 65),
    ("Green Beans (Habitchuelas)", "Vegetables", "kg", 75),
    ("Lettuce (Iceberg)", "Vegetables", "kg", 120),
    ("Lettuce (Romaine)", "Vegetables", "kg", 140),
    ("Bell Pepper (Green)", "Vegetables", "kg", 100),
    ("Bell Pepper (Red)", "Vegetables", "kg", 150),
    ("Cucumber", "Vegetables", "kg", 40),
    ("Radish (Labanos)", "Vegetables", "kg", 50),
    ("Mushroom (Oyster)", "Vegetables", "kg", 160),
    ("Mushroom (Button)", "Vegetables", "kg", 200),
    ("Spring Onion", "Vegetables", "kg", 80),
    ("Celery", "Vegetables", "kg", 120),
    ("Broccoli", "Vegetables", "kg", 180),
    ("Cauliflower", "Vegetables", "kg", 150),
    ("Spinach", "Vegetables", "kg", 100),
    ("Puso ng Saging (Banana Heart)", "Vegetables", "kg", 45),
    ("Langka (Green Jackfruit)", "Vegetables", "kg", 60),
    ("Talbos ng Sayote", "Vegetables", "kg", 50),
    ("Saluyot (Jute Leaves)", "Vegetables", "kg", 55),
    ("Alugbati (Malabar Spinach)", "Vegetables", "kg", 50),
    ("Sigarilyas (Winged Bean)", "Vegetables", "kg", 80),

    # ── Meat (20) ──
    ("Pork Liempo", "Meat", "kg", 325),
    ("Pork Kasim", "Meat", "kg", 280),
    ("Pork Pata", "Meat", "kg", 230),
    ("Pork Spare Ribs", "Meat", "kg", 290),
    ("Pork Tenderloin", "Meat", "kg", 340),
    ("Ground Pork", "Meat", "kg", 270),
    ("Pork Chop", "Meat", "kg", 300),
    ("Pork Belly (Skin-on)", "Meat", "kg", 310),
    ("Whole Chicken", "Meat", "kg", 190),
    ("Chicken Breast", "Meat", "kg", 210),
    ("Chicken Thigh", "Meat", "kg", 185),
    ("Chicken Wings", "Meat", "kg", 200),
    ("Chicken Liver", "Meat", "kg", 160),
    ("Chicken Gizzard", "Meat", "kg", 150),
    ("Beef Brisket", "Meat", "kg", 380),
    ("Beef Rump", "Meat", "kg", 400),
    ("Beef Round", "Meat", "kg", 420),
    ("Ground Beef", "Meat", "kg", 350),
    ("Beef Shank (Bulalo)", "Meat", "kg", 360),
    ("Goat Meat (Chevon)", "Meat", "kg", 400),

    # ── Fish & Seafood (35) ──
    ("Bangus (Milkfish)", "Fish & Seafood", "kg", 170),
    ("Tilapia", "Fish & Seafood", "kg", 120),
    ("Galunggong (Round Scad)", "Fish & Seafood", "kg", 160),
    ("Alumahan (Long-jawed Mackerel)", "Fish & Seafood", "kg", 200),
    ("Shrimp (Suahe)", "Fish & Seafood", "kg", 350),
    ("Shrimp (Tiger Prawn)", "Fish & Seafood", "kg", 500),
    ("Squid (Pusit)", "Fish & Seafood", "kg", 280),
    ("Maya-Maya (Red Snapper)", "Fish & Seafood", "kg", 350),
    ("Lapu-Lapu (Grouper)", "Fish & Seafood", "kg", 400),
    ("Dilis (Anchovies)", "Fish & Seafood", "kg", 180),
    ("Tulingan (Skipjack Tuna)", "Fish & Seafood", "kg", 200),
    ("Tambakol (Yellowfin Tuna)", "Fish & Seafood", "kg", 250),
    ("Tanigue (Spanish Mackerel)", "Fish & Seafood", "kg", 380),
    ("Hasa-Hasa (Short Mackerel)", "Fish & Seafood", "kg", 140),
    ("Espada (Swordfish)", "Fish & Seafood", "kg", 300),
    ("Pampano (Pompano)", "Fish & Seafood", "kg", 350),
    ("Bisugo (Threadfin Bream)", "Fish & Seafood", "kg", 220),
    ("Crab (Alimasag)", "Fish & Seafood", "kg", 280),
    ("Crab (Alimango)", "Fish & Seafood", "kg", 600),
    ("Tahong (Green Mussel)", "Fish & Seafood", "kg", 120),
    ("Talaba (Oyster)", "Fish & Seafood", "kg", 150),
    ("Halaan (Clam)", "Fish & Seafood", "kg", 130),
    ("Hipon (Small Shrimp)", "Fish & Seafood", "kg", 200),
    ("Tuyo (Dried Herring)", "Fish & Seafood", "kg", 200),
    ("Dried Dilis (Dried Anchovies)", "Fish & Seafood", "kg", 250),
    ("Dried Pusit (Dried Squid)", "Fish & Seafood", "kg", 400),
    ("Tinapa (Smoked Fish)", "Fish & Seafood", "kg", 180),
    ("Sardines (Fresh)", "Fish & Seafood", "kg", 140),
    ("Daing na Bangus", "Fish & Seafood", "kg", 220),
    ("Danggit (Rabbitfish, Dried)", "Fish & Seafood", "kg", 600),
    ("Sapsap (Ponyfish)", "Fish & Seafood", "kg", 120),
    ("Salay-Salay (Yellowstriped Scad)", "Fish & Seafood", "kg", 160),
    ("Tambakol Belly", "Fish & Seafood", "kg", 180),
    ("Kitang (Spotted Herring)", "Fish & Seafood", "kg", 150),
    ("Matambaka (Big-eye Scad)", "Fish & Seafood", "kg", 170),

    # ── Fruits (28) ──
    ("Banana (Lakatan)", "Fruits", "kg", 65),
    ("Banana (Latundan)", "Fruits", "kg", 50),
    ("Banana (Saba/Cooking)", "Fruits", "kg", 55),
    ("Calamansi", "Fruits", "kg", 80),
    ("Mango (Carabao)", "Fruits", "kg", 100),
    ("Mango (Indian)", "Fruits", "kg", 80),
    ("Papaya", "Fruits", "kg", 45),
    ("Pineapple", "Fruits", "kg", 50),
    ("Watermelon", "Fruits", "kg", 35),
    ("Melon (Cantaloupe)", "Fruits", "kg", 60),
    ("Apple (Fuji, Imported)", "Fruits", "kg", 150),
    ("Apple (Green, Imported)", "Fruits", "kg", 160),
    ("Orange (Imported)", "Fruits", "kg", 120),
    ("Grapes (Red, Imported)", "Fruits", "kg", 200),
    ("Grapes (Green, Imported)", "Fruits", "kg", 220),
    ("Pear (Imported)", "Fruits", "kg", 140),
    ("Lemon", "Fruits", "kg", 120),
    ("Avocado", "Fruits", "kg", 100),
    ("Guava (Bayabas)", "Fruits", "kg", 70),
    ("Coconut (Buko)", "Fruits", "pc", 40),
    ("Rambutan", "Fruits", "kg", 80),
    ("Lanzones", "Fruits", "kg", 90),
    ("Mangosteen", "Fruits", "kg", 120),
    ("Durian", "Fruits", "kg", 150),
    ("Jackfruit (Langka)", "Fruits", "kg", 70),
    ("Dalandan (Native Orange)", "Fruits", "kg", 60),
    ("Pomelo (Suha)", "Fruits", "kg", 80),
    ("Atis (Sugar Apple)", "Fruits", "kg", 100),

    # ── Poultry & Dairy (16) ──
    ("Egg (Large)", "Poultry & Dairy", "pc", 8),
    ("Egg (Medium)", "Poultry & Dairy", "pc", 7),
    ("Egg (Small)", "Poultry & Dairy", "pc", 6),
    ("Salted Egg (Itlog na Maalat)", "Poultry & Dairy", "pc", 12),
    ("Quail Egg (Itlog ng Pugo)", "Poultry & Dairy", "pc", 2),
    ("Fresh Milk (Full Cream)", "Poultry & Dairy", "L", 95),
    ("Fresh Milk (Low Fat)", "Poultry & Dairy", "L", 90),
    ("Evaporated Milk", "Poultry & Dairy", "can", 38),
    ("Condensed Milk", "Poultry & Dairy", "can", 42),
    ("Powdered Milk (Full Cream)", "Poultry & Dairy", "kg", 450),
    ("Cheese (Eden)", "Poultry & Dairy", "pc", 45),
    ("Cheese (Quickmelt)", "Poultry & Dairy", "kg", 280),
    ("Butter (Salted)", "Poultry & Dairy", "kg", 500),
    ("Margarine", "Poultry & Dairy", "kg", 180),
    ("Yogurt (Plain)", "Poultry & Dairy", "cup", 60),
    ("Kesong Puti (White Cheese)", "Poultry & Dairy", "pc", 50),

    # ── Spices & Condiments (22) ──
    ("Salt (Iodized)", "Spices & Condiments", "kg", 25),
    ("Salt (Rock)", "Spices & Condiments", "kg", 20),
    ("Black Pepper (Ground)", "Spices & Condiments", "kg", 600),
    ("White Pepper (Ground)", "Spices & Condiments", "kg", 700),
    ("Soy Sauce", "Spices & Condiments", "bottle", 30),
    ("Vinegar (Cane)", "Spices & Condiments", "bottle", 25),
    ("Vinegar (Coconut)", "Spices & Condiments", "bottle", 35),
    ("Fish Sauce (Patis)", "Spices & Condiments", "bottle", 30),
    ("Bagoong (Shrimp Paste)", "Spices & Condiments", "bottle", 80),
    ("Bagoong (Alamang)", "Spices & Condiments", "bottle", 70),
    ("Oyster Sauce", "Spices & Condiments", "bottle", 55),
    ("Banana Ketchup", "Spices & Condiments", "bottle", 35),
    ("Tomato Sauce", "Spices & Condiments", "bottle", 30),
    ("Bay Leaf (Laurel)", "Spices & Condiments", "pack", 15),
    ("Pandan Leaf", "Spices & Condiments", "bundle", 10),
    ("Lemongrass (Tanglad)", "Spices & Condiments", "bundle", 15),
    ("Turmeric (Luyang Dilaw)", "Spices & Condiments", "kg", 100),
    ("Annatto Seeds (Atsuete)", "Spices & Condiments", "pack", 10),
    ("Worcestershire Sauce", "Spices & Condiments", "bottle", 65),
    ("Chili Flakes", "Spices & Condiments", "pack", 25),
    ("Sesame Oil", "Spices & Condiments", "bottle", 85),
    ("Coco Aminos", "Spices & Condiments", "bottle", 120),

    # ── Canned & Processed (24) ──
    ("Sardines (Canned)", "Canned & Processed", "can", 22),
    ("Corned Beef (Canned)", "Canned & Processed", "can", 50),
    ("Tuna Flakes (Canned)", "Canned & Processed", "can", 35),
    ("Meat Loaf (Canned)", "Canned & Processed", "can", 40),
    ("Luncheon Meat", "Canned & Processed", "can", 85),
    ("Vienna Sausage", "Canned & Processed", "can", 30),
    ("Hotdog (Regular)", "Canned & Processed", "kg", 160),
    ("Hotdog (Jumbo)", "Canned & Processed", "kg", 200),
    ("Tocino", "Canned & Processed", "kg", 260),
    ("Longganisa", "Canned & Processed", "kg", 280),
    ("Tapa", "Canned & Processed", "kg", 350),
    ("Bacon", "Canned & Processed", "kg", 380),
    ("Ham", "Canned & Processed", "kg", 300),
    ("Bihon (Rice Noodles)", "Canned & Processed", "pack", 45),
    ("Sotanghon (Glass Noodles)", "Canned & Processed", "pack", 55),
    ("Canton Noodles", "Canned & Processed", "pack", 40),
    ("Misua (Thin Wheat Noodles)", "Canned & Processed", "pack", 50),
    ("Spaghetti Pasta", "Canned & Processed", "pack", 55),
    ("Macaroni Pasta", "Canned & Processed", "pack", 55),
    ("Instant Noodles", "Canned & Processed", "pack", 12),
    ("Instant Coffee (3-in-1)", "Canned & Processed", "pack", 8),
    ("Tablea (Chocolate)", "Canned & Processed", "pack", 60),
    ("Peanut Butter", "Canned & Processed", "bottle", 80),
    ("Dried Mango", "Canned & Processed", "pack", 120),

    # ── Other Essentials (21) ──
    ("Cooking Oil (Palm)", "Other Essentials", "L", 72),
    ("Cooking Oil (Coconut)", "Other Essentials", "L", 85),
    ("Cooking Oil (Canola)", "Other Essentials", "L", 120),
    ("Cooking Oil (Vegetable)", "Other Essentials", "L", 75),
    ("Refined Sugar", "Other Essentials", "kg", 75),
    ("Brown Sugar", "Other Essentials", "kg", 65),
    ("Muscovado Sugar", "Other Essentials", "kg", 80),
    ("Coconut Milk (Gata)", "Other Essentials", "can", 40),
    ("Coconut Cream", "Other Essentials", "can", 55),
    ("All-Purpose Flour", "Other Essentials", "kg", 48),
    ("Bread Flour", "Other Essentials", "kg", 52),
    ("Cornstarch", "Other Essentials", "kg", 65),
    ("Baking Powder", "Other Essentials", "can", 35),
    ("Baking Soda", "Other Essentials", "pack", 15),
    ("Tofu (Tokwa)", "Other Essentials", "pc", 15),
    ("Pandesal", "Other Essentials", "pc", 3),
    ("Lard (Mantika)", "Other Essentials", "kg", 80),
    ("Cassava (Kamoteng Kahoy)", "Other Essentials", "kg", 40),
    ("Desiccated Coconut", "Other Essentials", "kg", 160),
    ("Achuete Oil", "Other Essentials", "bottle", 35),
    ("Banana Chips", "Other Essentials", "pack", 60),
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
# One representative public market per region
# ---------------------------------------------------------------------------
SEED_MARKETS = [
    {"name": "Commonwealth Market", "region_code": "NCR", "type": "wet", "address": "Quezon City"},
    {"name": "Baguio City Public Market", "region_code": "CAR", "type": "wet", "address": "Baguio City"},
    {"name": "Vigan Public Market", "region_code": "R01", "type": "wet", "address": "Vigan, Ilocos Sur"},
    {"name": "Tuguegarao Center Market", "region_code": "R02", "type": "wet", "address": "Tuguegarao, Cagayan"},
    {"name": "Pampanga Public Market", "region_code": "R03", "type": "wet", "address": "San Fernando, Pampanga"},
    {"name": "Lucena Grand Central Market", "region_code": "R04A", "type": "wet", "address": "Lucena City, Quezon"},
    {
        "name": "Puerto Princesa Main Market",
        "region_code": "R04B",
        "type": "wet",
        "address": "Puerto Princesa, Palawan",
    },
    {"name": "Naga City Public Market", "region_code": "R05", "type": "wet", "address": "Naga City, Camarines Sur"},
    {"name": "Iloilo Terminal Market", "region_code": "R06", "type": "wet", "address": "Iloilo City"},
    {"name": "Carbon Public Market", "region_code": "R07", "type": "wet", "address": "Cebu City"},
    {"name": "Tacloban Public Market", "region_code": "R08", "type": "wet", "address": "Tacloban City, Leyte"},
    {"name": "Zamboanga City Central Market", "region_code": "R09", "type": "wet", "address": "Zamboanga City"},
    {"name": "Cogon Market", "region_code": "R10", "type": "wet", "address": "Cagayan de Oro, Misamis Oriental"},
    {"name": "Bankerohan Public Market", "region_code": "R11", "type": "wet", "address": "Davao City"},
    {"name": "General Santos Public Market", "region_code": "R12", "type": "wet", "address": "General Santos City"},
    {
        "name": "Butuan City Central Market",
        "region_code": "R13",
        "type": "wet",
        "address": "Butuan City, Agusan del Norte",
    },
    {"name": "Cotabato City Public Market", "region_code": "BARMM", "type": "wet", "address": "Cotabato City"},
]

# ---------------------------------------------------------------------------
# Volatility & spread multipliers per category
# ---------------------------------------------------------------------------
_CATEGORY_VOLATILITY: dict[str, float] = {
    "Rice": 0.006,
    "Vegetables": 0.025,
    "Meat": 0.008,
    "Fish & Seafood": 0.020,
    "Fruits": 0.018,
    "Poultry & Dairy": 0.010,
    "Spices & Condiments": 0.007,
    "Canned & Processed": 0.005,
    "Other Essentials": 0.007,
}

_CATEGORY_SPREAD: dict[str, Decimal] = {
    "Rice": Decimal("0.04"),
    "Vegetables": Decimal("0.08"),
    "Meat": Decimal("0.03"),
    "Fish & Seafood": Decimal("0.06"),
    "Fruits": Decimal("0.07"),
    "Poultry & Dairy": Decimal("0.04"),
    "Spices & Condiments": Decimal("0.03"),
    "Canned & Processed": Decimal("0.02"),
    "Other Essentials": Decimal("0.03"),
}

# Regional price adjustments (percentage of base price)
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
    """Return a deterministic float in [-1, 1] for reproducible price curves."""
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

        # Build all records in memory, then bulk-insert
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
                            source="DA-BPI",
                        )
                    )

        # Bulk-insert in batches to avoid memory pressure
        batch_size = 10000
        for i in range(0, len(records), batch_size):
            session.add_all(records[i : i + batch_size])
            await session.flush()

    await session.commit()
