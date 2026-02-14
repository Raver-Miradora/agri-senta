from app.scraping.types import RawPriceRecord

COMMODITY_NAME_MAP = {
    "well milled rice": "Well-Milled Rice",
    "red onion": "Red Onion",
    "pork liempo": "Pork Liempo",
}


def normalize_commodity_name(value: str) -> str:
    key = value.strip().lower()
    return COMMODITY_NAME_MAP.get(key, value.strip().title())


def clean_price_records(records: list[RawPriceRecord]) -> list[RawPriceRecord]:
    cleaned: list[RawPriceRecord] = []

    for record in records:
        if record.price_prevailing <= 0 or record.price_prevailing > 10000:
            continue

        normalized_name = normalize_commodity_name(record.commodity_name)
        cleaned.append(
            RawPriceRecord(
                commodity_name=normalized_name,
                market_name=record.market_name.strip(),
                region_code=record.region_code.strip().upper(),
                date=record.date,
                price_prevailing=round(record.price_prevailing, 2),
                price_low=record.price_low,
                price_high=record.price_high,
                source=record.source,
            )
        )

    return cleaned
