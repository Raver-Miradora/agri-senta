from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class RawPriceRecord:
    commodity_name: str
    market_name: str
    region_code: str
    date: date
    price_prevailing: float
    price_low: float | None = None
    price_high: float | None = None
    source: str = "DA"
