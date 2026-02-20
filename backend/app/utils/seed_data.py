"""Seed data for Agri-Senta: Lagonoy Municipal Agriculture Office.

Lagonoy is a coastal municipality in Camarines Sur (Bicol Region) facing
Lagonoy Gulf.  This seeds barangays as "regions", 210+ local commodities,
local markets, vendors, harvest records, and 90 days of realistic daily
price history.
"""

import hashlib
import math
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Commodity, DailyPrice, Market, Region
from app.models.harvest_record import HarvestRecord
from app.models.vendor import Vendor

# ---------------------------------------------------------------------------
# 38 Official Barangays of Lagonoy, Camarines Sur
#   code  -> short barangay code
#   island_group -> repurposed as "zone" (Poblacion / Coastal / Upland / Agricultural)
# ---------------------------------------------------------------------------
SEED_REGIONS = [
    {"name": "Agosais", "code": "AGO", "island_group": "Agricultural"},
    {"name": "Agpo-Camagong-Tabog", "code": "ACT", "island_group": "Upland"},
    {"name": "Amoguis", "code": "AMO", "island_group": "Agricultural"},
    {"name": "Balaton", "code": "BAL", "island_group": "Coastal"},
    {"name": "Binanuahan", "code": "BIN", "island_group": "Coastal"},
    {"name": "Bocogan", "code": "BOC", "island_group": "Upland"},
    {"name": "Burabod", "code": "BUR", "island_group": "Agricultural"},
    {"name": "Cabotonan", "code": "CAB", "island_group": "Agricultural"},
    {"name": "Dahat", "code": "DAH", "island_group": "Agricultural"},
    {"name": "Del Carmen", "code": "DLC", "island_group": "Agricultural"},
    {"name": "Genorangan", "code": "GEN", "island_group": "Upland"},
    {"name": "Gimagtocon", "code": "GIM", "island_group": "Coastal"},
    {"name": "Gubat", "code": "GUB", "island_group": "Coastal"},
    {"name": "Guibahoy", "code": "GUI", "island_group": "Upland"},
    {"name": "Himanag", "code": "HIM", "island_group": "Coastal"},
    {"name": "Kinahologan", "code": "KIN", "island_group": "Upland"},
    {"name": "Loho", "code": "LOH", "island_group": "Upland"},
    {"name": "Manamoc", "code": "MNA", "island_group": "Agricultural"},
    {"name": "Mangogon", "code": "MNG", "island_group": "Agricultural"},
    {"name": "Mapid", "code": "MAP", "island_group": "Agricultural"},
    {"name": "Olas", "code": "OLS", "island_group": "Coastal"},
    {"name": "Omalo", "code": "OMA", "island_group": "Agricultural"},
    {"name": "Panagan", "code": "PAN", "island_group": "Agricultural"},
    {"name": "Panicuan", "code": "PNC", "island_group": "Agricultural"},
    {"name": "Pinamihagan", "code": "PIN", "island_group": "Upland"},
    {"name": "San Francisco (Pob.)", "code": "SFR", "island_group": "Poblacion"},
    {"name": "San Isidro", "code": "SIS", "island_group": "Agricultural"},
    {"name": "San Isidro Norte (Pob.)", "code": "SIN", "island_group": "Poblacion"},
    {"name": "San Isidro Sur (Pob.)", "code": "SSR", "island_group": "Poblacion"},
    {"name": "San Rafael", "code": "SRF", "island_group": "Agricultural"},
    {"name": "San Ramon", "code": "SRM", "island_group": "Agricultural"},
    {"name": "San Roque", "code": "SRQ", "island_group": "Agricultural"},
    {"name": "San Sebastian", "code": "SSB", "island_group": "Upland"},
    {"name": "San Vicente (Pob.)", "code": "SVC", "island_group": "Poblacion"},
    {"name": "Santa Cruz (Pob.)", "code": "SCZ", "island_group": "Poblacion"},
    {"name": "Santa Maria (Pob.)", "code": "SMA", "island_group": "Poblacion"},
    {"name": "Saripongpong (Pob.)", "code": "SAR", "island_group": "Poblacion"},
    {"name": "Sipaco", "code": "SPC", "island_group": "Coastal"},
]

# ---------------------------------------------------------------------------
# 210+ locally relevant commodities for Lagonoy, Camarines Sur
#   Focus: Bicol staples, coconut products, Lagonoy Gulf seafood, local vegs
#   (name, category, unit, base_price_php)
# ---------------------------------------------------------------------------
_RAW_COMMODITIES: list[tuple[str, str, str, float]] = [
    # == Rice & Grains (15) ==
    ("Well-Milled Rice", "Rice & Grains", "kg", 48),
    ("Regular-Milled Rice", "Rice & Grains", "kg", 42),
    ("Premium Rice", "Rice & Grains", "kg", 56),
    ("NFA Rice", "Rice & Grains", "kg", 38),
    ("Glutinous Rice (Malagkit)", "Rice & Grains", "kg", 55),
    ("Sinandomeng Rice", "Rice & Grains", "kg", 52),
    ("Dinorado Rice", "Rice & Grains", "kg", 60),
    ("Brown Rice", "Rice & Grains", "kg", 62),
    ("Jasmine Rice", "Rice & Grains", "kg", 58),
    ("Corn Grits", "Rice & Grains", "kg", 35),
    ("Yellow Corn", "Rice & Grains", "kg", 28),
    ("White Corn", "Rice & Grains", "kg", 30),
    ("Mongo (Mung Bean)", "Rice & Grains", "kg", 90),
    ("Peanut (Mani)", "Rice & Grains", "kg", 110),
    ("Sorghum", "Rice & Grains", "kg", 45),

    # == Vegetables (35) ==
    ("Tomato", "Vegetables", "kg", 60),
    ("Red Onion", "Vegetables", "kg", 130),
    ("White Onion", "Vegetables", "kg", 100),
    ("Garlic (Local)", "Vegetables", "kg", 200),
    ("Garlic (Imported)", "Vegetables", "kg", 160),
    ("Eggplant (Talong)", "Vegetables", "kg", 55),
    ("Ampalaya (Bitter Gourd)", "Vegetables", "kg", 80),
    ("Squash (Kalabasa)", "Vegetables", "kg", 35),
    ("Kangkong (Water Spinach)", "Vegetables", "kg", 30),
    ("Sitaw (String Beans)", "Vegetables", "kg", 70),
    ("Chili Labuyo (Siling Labuyo)", "Vegetables", "kg", 250),
    ("Chili Siling Haba", "Vegetables", "kg", 120),
    ("Ginger (Luya)", "Vegetables", "kg", 120),
    ("Pechay (Bok Choy)", "Vegetables", "kg", 40),
    ("Pechay Tagalog", "Vegetables", "kg", 38),
    ("Sayote (Chayote)", "Vegetables", "kg", 35),
    ("Okra", "Vegetables", "kg", 65),
    ("Malunggay (Moringa)", "Vegetables", "kg", 60),
    ("Puso ng Saging (Banana Heart)", "Vegetables", "kg", 45),
    ("Saluyot (Jute Leaves)", "Vegetables", "kg", 55),
    ("Alugbati (Malabar Spinach)", "Vegetables", "kg", 50),
    ("Kalabasa Tops (Talbos)", "Vegetables", "kg", 32),
    ("Patola (Luffa/Sponge Gourd)", "Vegetables", "kg", 50),
    ("Upo (Bottle Gourd)", "Vegetables", "kg", 40),
    ("Bataw (Hyacinth Bean)", "Vegetables", "kg", 55),
    ("Sigarilyas (Winged Bean)", "Vegetables", "kg", 65),
    ("Labanos (Radish)", "Vegetables", "kg", 45),
    ("Repolyo (Cabbage)", "Vegetables", "kg", 55),
    ("Lettuce", "Vegetables", "kg", 80),
    ("Carrots", "Vegetables", "kg", 75),
    ("Bell Pepper (Green)", "Vegetables", "kg", 120),
    ("Bell Pepper (Red)", "Vegetables", "kg", 150),
    ("Cucumber", "Vegetables", "kg", 35),
    ("Singkamas (Jicama)", "Vegetables", "kg", 40),
    ("Toge (Mung Bean Sprouts)", "Vegetables", "kg", 30),
    ("Native Eggplant (Talong Bicolano)", "Vegetables", "kg", 60),

    # == Root Crops (10) ==
    ("Sweet Potato (Kamote)", "Root Crops", "kg", 40),
    ("Gabi (Taro)", "Root Crops", "kg", 45),
    ("Cassava (Kamoteng Kahoy)", "Root Crops", "kg", 30),
    ("Ube (Purple Yam)", "Root Crops", "kg", 100),
    ("Potato", "Root Crops", "kg", 70),
    ("Tugui (Lesser Yam)", "Root Crops", "kg", 50),
    ("Arrowroot (Uraro)", "Root Crops", "kg", 65),
    ("Yacon", "Root Crops", "kg", 80),
    ("Turmeric Root (Luyang Dilaw)", "Root Crops", "kg", 90),
    ("Taro Leaves (Laing)", "Root Crops", "kg", 55),

    # == Fruits (25) ==
    ("Banana (Saba/Cooking)", "Fruits", "kg", 55),
    ("Banana (Lakatan)", "Fruits", "kg", 65),
    ("Banana (Latundan)", "Fruits", "kg", 50),
    ("Calamansi", "Fruits", "kg", 80),
    ("Coconut (Buko)", "Fruits", "pc", 40),
    ("Coconut (Mature/Niyog)", "Fruits", "pc", 25),
    ("Papaya", "Fruits", "kg", 45),
    ("Pineapple", "Fruits", "kg", 50),
    ("Mango (Carabao)", "Fruits", "kg", 100),
    ("Jackfruit (Langka)", "Fruits", "kg", 70),
    ("Watermelon", "Fruits", "kg", 35),
    ("Avocado", "Fruits", "kg", 100),
    ("Guava (Bayabas)", "Fruits", "kg", 40),
    ("Santol", "Fruits", "kg", 35),
    ("Rambutan", "Fruits", "kg", 80),
    ("Lanzones", "Fruits", "kg", 90),
    ("Durian", "Fruits", "kg", 150),
    ("Pomelo (Suha)", "Fruits", "pc", 60),
    ("Atis (Sugar Apple)", "Fruits", "kg", 70),
    ("Chico (Sapodilla)", "Fruits", "kg", 60),
    ("Guyabano (Soursop)", "Fruits", "kg", 90),
    ("Melon (Cantaloupe)", "Fruits", "kg", 50),
    ("Dalandan (Green Orange)", "Fruits", "kg", 45),
    ("Dalanghita (Mandarin)", "Fruits", "kg", 55),
    ("Star Apple (Kaimito)", "Fruits", "kg", 50),

    # == Fish & Seafood - Fresh (25) ==
    ("Galunggong (Round Scad)", "Fish & Seafood", "kg", 160),
    ("Tulingan (Skipjack Tuna)", "Fish & Seafood", "kg", 200),
    ("Tambakol (Yellowfin Tuna)", "Fish & Seafood", "kg", 250),
    ("Bangus (Milkfish)", "Fish & Seafood", "kg", 170),
    ("Tilapia", "Fish & Seafood", "kg", 120),
    ("Lapu-Lapu (Grouper)", "Fish & Seafood", "kg", 400),
    ("Maya-Maya (Red Snapper)", "Fish & Seafood", "kg", 350),
    ("Hipon (Shrimp)", "Fish & Seafood", "kg", 280),
    ("Pusit (Squid)", "Fish & Seafood", "kg", 260),
    ("Dilis (Anchovies)", "Fish & Seafood", "kg", 180),
    ("Hasa-Hasa (Short Mackerel)", "Fish & Seafood", "kg", 140),
    ("Tanigue (Spanish Mackerel)", "Fish & Seafood", "kg", 380),
    ("Bisugo (Threadfin Bream)", "Fish & Seafood", "kg", 220),
    ("Espada (Hairtail)", "Fish & Seafood", "kg", 180),
    ("Salinyasi (Indian Sardine)", "Fish & Seafood", "kg", 130),
    ("Kitang (Rabbitfish)", "Fish & Seafood", "kg", 200),
    ("Banak (Mullet)", "Fish & Seafood", "kg", 160),
    ("Matang Baka (Big-Eye Scad)", "Fish & Seafood", "kg", 170),
    ("Talakitok (Trevally)", "Fish & Seafood", "kg", 300),
    ("Salay-Salay (Yellow-Striped Scad)", "Fish & Seafood", "kg", 150),
    ("Tamban (Sardine)", "Fish & Seafood", "kg", 120),
    ("Katambak (Emperor Fish)", "Fish & Seafood", "kg", 240),
    ("Sapsap (Pony Fish)", "Fish & Seafood", "kg", 110),
    ("Dangit (Spinefoot)", "Fish & Seafood", "kg", 210),
    ("Dalagang-Bukid (Fusilier)", "Fish & Seafood", "kg", 190),

    # == Dried / Preserved Fish (10) ==
    ("Tuyo (Dried Herring)", "Dried Fish", "kg", 200),
    ("Tinapa (Smoked Fish)", "Dried Fish", "kg", 180),
    ("Dried Dilis", "Dried Fish", "kg", 250),
    ("Dried Pusit", "Dried Fish", "kg", 300),
    ("Buwad (Dried Fish, assorted)", "Dried Fish", "kg", 210),
    ("Daing na Bangus", "Dried Fish", "kg", 240),
    ("Dried Galunggong", "Dried Fish", "kg", 220),
    ("Dried Danggit", "Dried Fish", "kg", 350),
    ("Burong Isda (Fermented Fish)", "Dried Fish", "kg", 150),
    ("Ginamos (Fish Paste)", "Dried Fish", "kg", 120),

    # == Shellfish & Crustaceans (10) ==
    ("Tahong (Green Mussel)", "Shellfish", "kg", 120),
    ("Talaba (Oyster)", "Shellfish", "kg", 150),
    ("Halaan (Clam)", "Shellfish", "kg", 100),
    ("Kuhol (Golden Apple Snail)", "Shellfish", "kg", 60),
    ("Suahe (Small Shrimp)", "Shellfish", "kg", 200),
    ("Sugpo (Tiger Prawn)", "Shellfish", "kg", 450),
    ("Alimango (Mud Crab)", "Shellfish", "kg", 500),
    ("Alimasag (Blue Crab)", "Shellfish", "kg", 280),
    ("Litob (Sea Snail)", "Shellfish", "kg", 90),
    ("Abuos (Sea Urchin)", "Shellfish", "kg", 200),

    # == Meat & Poultry (15) ==
    ("Pork Liempo", "Meat & Poultry", "kg", 325),
    ("Pork Kasim", "Meat & Poultry", "kg", 280),
    ("Pork Pata", "Meat & Poultry", "kg", 230),
    ("Ground Pork", "Meat & Poultry", "kg", 270),
    ("Pork Loin (Lomo)", "Meat & Poultry", "kg", 310),
    ("Whole Chicken", "Meat & Poultry", "kg", 190),
    ("Chicken Breast", "Meat & Poultry", "kg", 210),
    ("Chicken Thigh", "Meat & Poultry", "kg", 185),
    ("Chicken Wings", "Meat & Poultry", "kg", 175),
    ("Ground Chicken", "Meat & Poultry", "kg", 200),
    ("Beef Brisket", "Meat & Poultry", "kg", 380),
    ("Beef Shank (Bulalo)", "Meat & Poultry", "kg", 360),
    ("Carabeef (Kalabaw)", "Meat & Poultry", "kg", 320),
    ("Goat Meat (Chevon)", "Meat & Poultry", "kg", 400),
    ("Duck (Itik)", "Meat & Poultry", "kg", 220),

    # == Coconut Products - Bicol specialty (10) ==
    ("Copra", "Coconut Products", "kg", 38),
    ("Coconut Oil (Virgin)", "Coconut Products", "L", 180),
    ("Coconut Milk (Gata)", "Coconut Products", "L", 80),
    ("Coconut Cream", "Coconut Products", "L", 110),
    ("Desiccated Coconut", "Coconut Products", "kg", 160),
    ("Coco Sugar", "Coconut Products", "kg", 200),
    ("Nata de Coco", "Coconut Products", "kg", 70),
    ("Coconut Flour", "Coconut Products", "kg", 130),
    ("Coconut Vinegar (Sukang Tuba)", "Coconut Products", "bottle", 40),
    ("Coconut Water (Bottled)", "Coconut Products", "bottle", 25),

    # == Eggs & Dairy (10) ==
    ("Egg (Large)", "Eggs & Dairy", "pc", 8),
    ("Egg (Medium)", "Eggs & Dairy", "pc", 7),
    ("Egg (Small)", "Eggs & Dairy", "pc", 6),
    ("Salted Egg (Itlog na Maalat)", "Eggs & Dairy", "pc", 12),
    ("Balut", "Eggs & Dairy", "pc", 18),
    ("Penoy", "Eggs & Dairy", "pc", 15),
    ("Evaporated Milk", "Eggs & Dairy", "can", 38),
    ("Condensed Milk", "Eggs & Dairy", "can", 42),
    ("Powdered Milk", "Eggs & Dairy", "sachet", 12),
    ("Kesong Puti (White Cheese)", "Eggs & Dairy", "pc", 30),

    # == Spices & Condiments (15) ==
    ("Salt (Iodized)", "Spices & Condiments", "kg", 25),
    ("Soy Sauce", "Spices & Condiments", "bottle", 30),
    ("Vinegar (Coconut)", "Spices & Condiments", "bottle", 35),
    ("Vinegar (Cane)", "Spices & Condiments", "bottle", 28),
    ("Fish Sauce (Patis)", "Spices & Condiments", "bottle", 30),
    ("Bagoong (Shrimp Paste)", "Spices & Condiments", "bottle", 80),
    ("Bagoong Alamang", "Spices & Condiments", "bottle", 65),
    ("Cooking Oil (Coconut)", "Spices & Condiments", "L", 85),
    ("Cooking Oil (Palm)", "Spices & Condiments", "L", 72),
    ("Cooking Oil (Canola)", "Spices & Condiments", "L", 110),
    ("Banana Ketchup", "Spices & Condiments", "bottle", 35),
    ("Tomato Sauce", "Spices & Condiments", "bottle", 30),
    ("Oyster Sauce", "Spices & Condiments", "bottle", 50),
    ("Black Pepper (Ground)", "Spices & Condiments", "pack", 15),
    ("MSG (Vetsin)", "Spices & Condiments", "pack", 8),

    # == Dried Goods & Pantry (15) ==
    ("Sugar (White/Refined)", "Dried Goods", "kg", 55),
    ("Sugar (Brown/Washed)", "Dried Goods", "kg", 50),
    ("Muscovado Sugar", "Dried Goods", "kg", 90),
    ("All-Purpose Flour", "Dried Goods", "kg", 50),
    ("Cornstarch", "Dried Goods", "pack", 15),
    ("Pancit Canton (Dried Noodles)", "Dried Goods", "pack", 12),
    ("Pancit Bihon", "Dried Goods", "pack", 35),
    ("Sotanghon (Glass Noodles)", "Dried Goods", "pack", 40),
    ("Misua", "Dried Goods", "pack", 30),
    ("Dried Red Beans", "Dried Goods", "kg", 100),
    ("Sago (Tapioca Pearls)", "Dried Goods", "kg", 55),
    ("Coffee (Local Ground)", "Dried Goods", "pack", 25),
    ("Coffee (3-in-1 Sachet)", "Dried Goods", "sachet", 8),
    ("Cocoa Tablea", "Dried Goods", "pack", 60),
    ("Instant Noodles", "Dried Goods", "pack", 10),

    # == Canned Goods (10) ==
    ("Sardines (Canned)", "Canned Goods", "can", 22),
    ("Corned Beef", "Canned Goods", "can", 45),
    ("Meatloaf (Canned)", "Canned Goods", "can", 35),
    ("Vienna Sausage", "Canned Goods", "can", 30),
    ("Tuna Flakes (Canned)", "Canned Goods", "can", 32),
    ("Liver Spread", "Canned Goods", "can", 25),
    ("Luncheon Meat", "Canned Goods", "can", 65),
    ("Pork & Beans", "Canned Goods", "can", 25),
    ("Canned Milkfish", "Canned Goods", "can", 55),
    ("Canned Coconut Milk", "Canned Goods", "can", 40),

    # == Beverages (5) ==
    ("Softdrinks (Per Bottle)", "Beverages", "bottle", 15),
    ("Bottled Water (500ml)", "Beverages", "bottle", 12),
    ("Juice (Sachet)", "Beverages", "sachet", 8),
    ("Instant Coffee (Sachet)", "Beverages", "sachet", 7),
    ("Powdered Juice (Sachet)", "Beverages", "sachet", 10),
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
    {"name": "Lagonoy Public Market", "region_code": "SFR", "type": "wet", "address": "San Francisco (Pob.), Lagonoy, Camarines Sur"},
    {"name": "Lagonoy Dry Goods Market", "region_code": "SIN", "type": "dry", "address": "San Isidro Norte (Pob.), Lagonoy, Camarines Sur"},
    {"name": "Binanuahan Fish Landing", "region_code": "BIN", "type": "fish_port", "address": "Binanuahan, Lagonoy, Camarines Sur"},
    {"name": "Himanag Coastal Market", "region_code": "HIM", "type": "wet", "address": "Himanag, Lagonoy, Camarines Sur"},
    {"name": "San Isidro Buying Station", "region_code": "SIS", "type": "buying_station", "address": "San Isidro, Lagonoy, Camarines Sur"},
]

# ---------------------------------------------------------------------------
# Vendors per market
# ---------------------------------------------------------------------------
SEED_VENDORS = [
    # Lagonoy Public Market vendors
    {"name": "Aling Nena's Sari-Sari", "stall_number": "A-01", "market_index": 0, "commodity_type": "Rice & Grains", "contact_number": "0917-123-4501", "is_active": True},
    {"name": "Mang Tonyo's Meat Shop", "stall_number": "A-02", "market_index": 0, "commodity_type": "Meat & Poultry", "contact_number": "0918-234-5601", "is_active": True},
    {"name": "Bebang's Vegetables", "stall_number": "A-03", "market_index": 0, "commodity_type": "Vegetables", "contact_number": "0919-345-6701", "is_active": True},
    {"name": "Lola Caring's Fruits", "stall_number": "A-04", "market_index": 0, "commodity_type": "Fruits", "contact_number": "0920-456-7801", "is_active": True},
    {"name": "Pedro's Coconut Products", "stall_number": "A-05", "market_index": 0, "commodity_type": "Coconut Products", "contact_number": "0921-567-8901", "is_active": True},
    {"name": "Maria's Spices & Condiments", "stall_number": "A-06", "market_index": 0, "commodity_type": "Spices & Condiments", "contact_number": "0922-678-9012", "is_active": True},
    {"name": "Josie's Egg Stand", "stall_number": "A-07", "market_index": 0, "commodity_type": "Eggs & Dairy", "contact_number": "0923-789-0123", "is_active": True},
    {"name": "Tita Luz General Store", "stall_number": "A-08", "market_index": 0, "commodity_type": "Canned Goods", "contact_number": "0924-890-1234", "is_active": True},
    {"name": "Manay Rosa's Rice Stall", "stall_number": "A-09", "market_index": 0, "commodity_type": "Rice & Grains", "contact_number": "0925-901-2345", "is_active": True},
    {"name": "Boy Ampalaya", "stall_number": "A-10", "market_index": 0, "commodity_type": "Vegetables", "contact_number": "0926-012-3456", "is_active": True},
    # Lagonoy Dry Goods Market vendors
    {"name": "Jun's General Merchandise", "stall_number": "B-01", "market_index": 1, "commodity_type": "Dried Goods", "contact_number": "0917-111-2201", "is_active": True},
    {"name": "Aling Belen's Dried Fish", "stall_number": "B-02", "market_index": 1, "commodity_type": "Dried Fish", "contact_number": "0918-222-3301", "is_active": True},
    {"name": "Tindahan ni Inday", "stall_number": "B-03", "market_index": 1, "commodity_type": "Spices & Condiments", "contact_number": "0919-333-4401", "is_active": True},
    {"name": "Ate Glo's Grocery", "stall_number": "B-04", "market_index": 1, "commodity_type": "Canned Goods", "contact_number": "0920-444-5501", "is_active": True},
    {"name": "Mang Erning's Rice Depot", "stall_number": "B-05", "market_index": 1, "commodity_type": "Rice & Grains", "contact_number": "0921-555-6601", "is_active": True},
    {"name": "Nena's Bagoong House", "stall_number": "B-06", "market_index": 1, "commodity_type": "Spices & Condiments", "contact_number": "0922-666-7701", "is_active": True},
    # Binanuahan Fish Landing vendors
    {"name": "Kapitan Ben's Fresh Catch", "stall_number": "C-01", "market_index": 2, "commodity_type": "Fish & Seafood", "contact_number": "0917-100-2001", "is_active": True},
    {"name": "Mang Andoy's Seafood", "stall_number": "C-02", "market_index": 2, "commodity_type": "Fish & Seafood", "contact_number": "0918-200-3001", "is_active": True},
    {"name": "Nanay Perla's Shellfish", "stall_number": "C-03", "market_index": 2, "commodity_type": "Shellfish", "contact_number": "0919-300-4001", "is_active": True},
    {"name": "Boy Pusit Fish Dealer", "stall_number": "C-04", "market_index": 2, "commodity_type": "Fish & Seafood", "contact_number": "0920-400-5001", "is_active": True},
    {"name": "Kuya Romy's Dried Fish", "stall_number": "C-05", "market_index": 2, "commodity_type": "Dried Fish", "contact_number": "0921-500-6001", "is_active": True},
    # Himanag Coastal Market vendors
    {"name": "Aling Mila's Fish Stall", "stall_number": "D-01", "market_index": 3, "commodity_type": "Fish & Seafood", "contact_number": "0917-101-2002", "is_active": True},
    {"name": "Mang Isko's Vegetables", "stall_number": "D-02", "market_index": 3, "commodity_type": "Vegetables", "contact_number": "0918-202-3002", "is_active": True},
    {"name": "Nanay Betty's Sari-Sari", "stall_number": "D-03", "market_index": 3, "commodity_type": "Dried Goods", "contact_number": "0919-303-4002", "is_active": True},
    {"name": "Tatay Domeng's Meat", "stall_number": "D-04", "market_index": 3, "commodity_type": "Meat & Poultry", "contact_number": "0920-404-5002", "is_active": True},
    # San Isidro Buying Station vendors
    {"name": "San Isidro Farmers' Coop", "stall_number": "E-01", "market_index": 4, "commodity_type": "Root Crops", "contact_number": "0917-102-2003", "is_active": True},
    {"name": "Tatay Poldo's Rice Mill", "stall_number": "E-02", "market_index": 4, "commodity_type": "Rice & Grains", "contact_number": "0918-203-3003", "is_active": True},
    {"name": "Kuya Danny's Copra", "stall_number": "E-03", "market_index": 4, "commodity_type": "Coconut Products", "contact_number": "0919-304-4003", "is_active": True},
    {"name": "Ate Marites Fruit Stand", "stall_number": "E-04", "market_index": 4, "commodity_type": "Fruits", "contact_number": "0920-405-5003", "is_active": True},
    {"name": "Lolo Tinong's Farm Fresh", "stall_number": "E-05", "market_index": 4, "commodity_type": "Vegetables", "contact_number": "0921-506-6003", "is_active": True},
]

# ---------------------------------------------------------------------------
# Volatility & spread multipliers per category
# ---------------------------------------------------------------------------
_CATEGORY_VOLATILITY: dict[str, float] = {
    "Rice & Grains": 0.006,
    "Vegetables": 0.025,
    "Root Crops": 0.018,
    "Fruits": 0.018,
    "Fish & Seafood": 0.022,
    "Dried Fish": 0.010,
    "Shellfish": 0.025,
    "Meat & Poultry": 0.008,
    "Coconut Products": 0.015,
    "Eggs & Dairy": 0.010,
    "Spices & Condiments": 0.007,
    "Dried Goods": 0.006,
    "Canned Goods": 0.004,
    "Beverages": 0.003,
}

_CATEGORY_SPREAD: dict[str, Decimal] = {
    "Rice & Grains": Decimal("0.04"),
    "Vegetables": Decimal("0.08"),
    "Root Crops": Decimal("0.06"),
    "Fruits": Decimal("0.07"),
    "Fish & Seafood": Decimal("0.07"),
    "Dried Fish": Decimal("0.05"),
    "Shellfish": Decimal("0.08"),
    "Meat & Poultry": Decimal("0.03"),
    "Coconut Products": Decimal("0.05"),
    "Eggs & Dairy": Decimal("0.04"),
    "Spices & Condiments": Decimal("0.03"),
    "Dried Goods": Decimal("0.03"),
    "Canned Goods": Decimal("0.02"),
    "Beverages": Decimal("0.02"),
}

# Barangay zone price adjustments (38 barangays)
_REGION_PCT: dict[str, float] = {
    # Poblacion barangays (slight premium - town center)
    "SFR": 0.03, "SIN": 0.03, "SSR": 0.02, "SVC": 0.02, "SCZ": 0.01, "SMA": 0.02, "SAR": 0.01,
    # Agricultural barangays (slightly cheaper - closer to farms)
    "AGO": -0.02, "AMO": -0.02, "BUR": -0.03, "CAB": -0.02, "DAH": -0.03,
    "DLC": -0.02, "MNA": -0.03, "MNG": -0.02, "MAP": -0.02, "OMA": -0.03,
    "PAN": -0.02, "PNC": -0.02, "SIS": -0.01, "SRF": -0.02, "SRM": -0.02,
    "SRQ": -0.02,
    # Coastal barangays (fish cheaper, produce slightly higher)
    "BAL": -0.01, "BIN": -0.01, "GIM": 0.00, "GUB": -0.01, "HIM": 0.00,
    "OLS": -0.01, "SPC": 0.00,
    # Upland barangays (transport premium)
    "ACT": -0.04, "BOC": -0.04, "GEN": -0.03, "GUI": -0.04, "KIN": -0.04,
    "LOH": -0.04, "PIN": -0.03, "SSB": -0.03,
}

HISTORY_DAYS = 90

# ---------------------------------------------------------------------------
# Harvest data configuration
# ---------------------------------------------------------------------------
_HARVESTABLE_CATEGORIES = {"Rice & Grains", "Vegetables", "Root Crops", "Fruits", "Coconut Products"}
_AGRICULTURAL_BARANGAY_CODES = [
    "AGO", "AMO", "BUR", "CAB", "DAH", "DLC", "MNA", "MNG", "MAP",
    "OMA", "PAN", "PNC", "SIS", "SRF", "SRM", "SRQ",
]
_FARMER_FIRST_NAMES = [
    "Juan", "Pedro", "Maria", "Jose", "Rosa", "Antonio", "Elena", "Ricardo",
    "Luisa", "Manuel", "Carmen", "Roberto", "Teresa", "Francisco", "Gloria",
    "Eduardo", "Lourdes", "Ramon", "Estrella", "Danilo", "Nena", "Ernesto",
    "Celia", "Virgilio", "Aida", "Reynaldo", "Corazon", "Domingo", "Fe",
    "Fernando", "Dolores", "Angelo", "Paz", "Benjamin", "Norma",
]
_FARMER_LAST_NAMES = [
    "Santos", "Reyes", "Cruz", "Bautista", "Ocampo", "Mendoza", "Rivera",
    "Torres", "Flores", "Garcia", "Ramos", "Aquino", "Hernandez", "Lopez",
    "Dela Cruz", "Villanueva", "De Leon", "Castillo", "Pangilinan", "Enriquez",
    "Magno", "Perez", "Santiago", "Dizon", "Salazar", "Soriano", "Imperial",
    "Borja", "Ponce", "Almonte",
]
_SEASONS = ["Dry", "Wet", "Year-Round"]


def _deterministic_noise(seed_str: str, day: int) -> float:
    """Return a deterministic float in [-1, 1] for reproducible price curves."""
    raw = hashlib.md5(f"{seed_str}:{day}".encode()).hexdigest()  # noqa: S324
    return (int(raw[:8], 16) / 0xFFFFFFFF) * 2 - 1


def _det_random(seed_str: str, index: int) -> float:
    """Return a deterministic float in [0, 1)."""
    raw = hashlib.md5(f"{seed_str}:{index}".encode()).hexdigest()  # noqa: S324
    return int(raw[:8], 16) / 0xFFFFFFFF


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

    # ------------------------------------------------------------------
    # 5. Vendors
    # ------------------------------------------------------------------
    vendor_count = await session.scalar(select(func.count(Vendor.id)))
    if vendor_count == 0:
        market_rows = await session.execute(select(Market))
        market_list = list(market_rows.scalars().all())

        vendor_records = []
        for v in SEED_VENDORS:
            market_idx = v["market_index"]
            if market_idx < len(market_list):
                vendor_records.append(
                    Vendor(
                        name=v["name"],
                        stall_number=v["stall_number"],
                        market_id=market_list[market_idx].id,
                        commodity_type=v["commodity_type"],
                        contact_number=v["contact_number"],
                        is_active=v["is_active"],
                    )
                )
        session.add_all(vendor_records)
        await session.flush()

    # ------------------------------------------------------------------
    # 6. Harvest records (realistic crop yields for agricultural barangays)
    # ------------------------------------------------------------------
    harvest_count = await session.scalar(select(func.count(HarvestRecord.id)))
    if harvest_count == 0:
        region_rows = await session.execute(select(Region))
        region_by_code = {r.code: r for r in region_rows.scalars().all()}

        commodity_rows = await session.execute(select(Commodity))
        all_commodities = {row.name: row for row in commodity_rows.scalars().all()}

        # Pick harvestable commodities
        harvestable = [
            (name, cat, unit, price)
            for name, cat, unit, price in _RAW_COMMODITIES
            if cat in _HARVESTABLE_CATEGORIES
        ]

        harvest_records: list[HarvestRecord] = []
        today = datetime.now(UTC).date()

        for brgy_code in _AGRICULTURAL_BARANGAY_CODES:
            region_obj = region_by_code.get(brgy_code)
            if region_obj is None:
                continue

            # Each agricultural barangay gets 8-15 harvest records
            n_records = 8 + int(_det_random(f"harvest-count-{brgy_code}", 0) * 8)

            for i in range(n_records):
                # Pick a harvestable commodity deterministically
                commodity_idx = int(_det_random(f"{brgy_code}-crop", i) * len(harvestable))
                crop_name, crop_cat, _, _ = harvestable[commodity_idx]
                commodity_obj = all_commodities.get(crop_name)
                if commodity_obj is None:
                    continue

                # Quantity depends on category
                if crop_cat == "Rice & Grains":
                    qty = 500 + _det_random(f"{brgy_code}-qty", i) * 4500
                elif crop_cat == "Coconut Products":
                    qty = 200 + _det_random(f"{brgy_code}-qty", i) * 3000
                elif crop_cat == "Vegetables":
                    qty = 50 + _det_random(f"{brgy_code}-qty", i) * 500
                elif crop_cat == "Root Crops":
                    qty = 100 + _det_random(f"{brgy_code}-qty", i) * 1000
                else:  # Fruits
                    qty = 80 + _det_random(f"{brgy_code}-qty", i) * 800

                # Area 0.25-5.0 hectares
                area = 0.25 + _det_random(f"{brgy_code}-area", i) * 4.75

                # Season
                season_idx = int(_det_random(f"{brgy_code}-season", i) * len(_SEASONS))
                season = _SEASONS[season_idx]

                # Harvest date: within last 180 days
                days_ago = int(_det_random(f"{brgy_code}-date", i) * 180)
                harvest_date = today - timedelta(days=days_ago)

                # Farmer name
                fn_idx = int(_det_random(f"{brgy_code}-fn", i) * len(_FARMER_FIRST_NAMES))
                ln_idx = int(_det_random(f"{brgy_code}-ln", i) * len(_FARMER_LAST_NAMES))
                farmer_name = f"{_FARMER_FIRST_NAMES[fn_idx]} {_FARMER_LAST_NAMES[ln_idx]}"

                harvest_records.append(
                    HarvestRecord(
                        region_id=region_obj.id,
                        commodity_id=commodity_obj.id,
                        quantity_kg=Decimal(str(round(qty, 2))),
                        area_hectares=Decimal(str(round(area, 4))),
                        season=season,
                        harvest_date=harvest_date,
                        farmer_name=farmer_name,
                        notes=f"Harvest from Brgy. {region_obj.name}, Lagonoy",
                    )
                )

        session.add_all(harvest_records)
        await session.flush()

    await session.commit()
