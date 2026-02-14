from time import perf_counter

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.scraping.data_cleaner import clean_price_records
from app.scraping.data_loader import upsert_daily_prices
from app.scraping.scrape_logger import create_scrape_log
from app.scraping.scraper_da import scrape_da_prices
from app.scraping.scraper_psa import scrape_psa_prices

settings = get_settings()


async def run_ingestion_pipeline(source: str = "DA") -> dict[str, int | str]:
    started_at = perf_counter()

    async with AsyncSessionLocal() as session:
        try:
            if source.upper() == "PSA":
                raw_records = await scrape_psa_prices(settings.psa_api_url)
                source_name = "PSA"
            else:
                raw_records = await scrape_da_prices(settings.da_scrape_url)
                source_name = "DA"

            cleaned_records = clean_price_records(raw_records)
            rows_ingested = await upsert_daily_prices(session, cleaned_records)
            duration = perf_counter() - started_at

            await create_scrape_log(
                session,
                source=source_name,
                status="success",
                rows_ingested=rows_ingested,
                error_message=None,
                duration_seconds=duration,
            )

            return {"status": "success", "source": source_name, "rows_ingested": rows_ingested}
        except Exception as exc:
            duration = perf_counter() - started_at
            await create_scrape_log(
                session,
                source=source.upper(),
                status="failed",
                rows_ingested=0,
                error_message=str(exc),
                duration_seconds=duration,
            )
            raise
