from datetime import date

from app.scraping.data_cleaner import clean_price_records, normalize_commodity_name
from app.scraping.types import RawPriceRecord


def test_normalize_known_commodity_name() -> None:
    assert normalize_commodity_name("well milled rice") == "Well-Milled Rice"
    assert normalize_commodity_name("RED ONION") == "Red Onion"


def test_normalize_unknown_commodity_name_title_cases() -> None:
    assert normalize_commodity_name("bangus fillet") == "Bangus Fillet"


def test_clean_price_records_removes_invalid_prices() -> None:
    records = [
        RawPriceRecord(
            commodity_name="Well-Milled Rice",
            market_name="Test Market",
            region_code="NCR",
            date=date(2026, 1, 1),
            price_prevailing=48.0,
        ),
        RawPriceRecord(
            commodity_name="Bad Item",
            market_name="Test Market",
            region_code="NCR",
            date=date(2026, 1, 1),
            price_prevailing=-5.0,  # invalid
        ),
        RawPriceRecord(
            commodity_name="Overpriced",
            market_name="Test Market",
            region_code="NCR",
            date=date(2026, 1, 1),
            price_prevailing=99999.0,  # over 10k limit
        ),
    ]

    cleaned = clean_price_records(records)
    assert len(cleaned) == 1
    assert cleaned[0].commodity_name == "Well-Milled Rice"


def test_clean_price_records_normalises_whitespace() -> None:
    record = RawPriceRecord(
        commodity_name="  pork liempo  ",
        market_name="  Carbon Public Market ",
        region_code="  r07  ",
        date=date(2026, 2, 1),
        price_prevailing=320.0,
    )

    cleaned = clean_price_records([record])
    assert cleaned[0].commodity_name == "Pork Liempo"
    assert cleaned[0].market_name == "Carbon Public Market"
    assert cleaned[0].region_code == "R07"
