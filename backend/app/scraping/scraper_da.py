from datetime import UTC, date, datetime

import httpx
from bs4 import BeautifulSoup

from app.scraping.types import RawPriceRecord


async def scrape_da_prices(url: str, timeout_seconds: int = 30) -> list[RawPriceRecord]:
    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        response = await client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table_rows = soup.select("table tr")

    records: list[RawPriceRecord] = []
    scrape_date = datetime.now(UTC).date()

    for row in table_rows[1:]:
        columns = [column.get_text(strip=True) for column in row.find_all("td")]
        if len(columns) < 5:
            continue

        commodity_name = columns[0]
        market_name = columns[1]
        region_code = columns[2]

        try:
            prevailing = float(columns[3].replace(",", ""))
        except ValueError:
            continue

        records.append(
            RawPriceRecord(
                commodity_name=commodity_name,
                market_name=market_name,
                region_code=region_code,
                date=scrape_date,
                price_prevailing=prevailing,
                source="DA",
            )
        )

    return records
