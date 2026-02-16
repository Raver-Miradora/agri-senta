import asyncio
from datetime import UTC, datetime
from functools import partial

import pandas as pd

from app.scraping.types import RawPriceRecord


def _read_csv_sync(csv_url: str) -> pd.DataFrame:
    """Read CSV in a way that can be offloaded to a thread."""
    return pd.read_csv(csv_url)


async def scrape_psa_prices(csv_url: str) -> list[RawPriceRecord]:
    loop = asyncio.get_running_loop()
    dataframe = await loop.run_in_executor(None, partial(_read_csv_sync, csv_url))
    now_date = datetime.now(UTC).date()

    records: list[RawPriceRecord] = []
    required_columns = {"commodity", "market", "region_code", "price_prevailing"}

    if not required_columns.issubset(set(dataframe.columns.str.lower())):
        return records

    normalized_columns = {column.lower(): column for column in dataframe.columns}

    for _, row in dataframe.iterrows():
        try:
            records.append(
                RawPriceRecord(
                    commodity_name=str(row[normalized_columns["commodity"]]),
                    market_name=str(row[normalized_columns["market"]]),
                    region_code=str(row[normalized_columns["region_code"]]),
                    date=now_date,
                    price_prevailing=float(row[normalized_columns["price_prevailing"]]),
                    source="PSA",
                )
            )
        except (TypeError, ValueError):
            continue

    return records
