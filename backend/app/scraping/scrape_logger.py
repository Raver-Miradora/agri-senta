from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ScrapeLog


async def create_scrape_log(
    session: AsyncSession,
    *,
    source: str,
    status: str,
    rows_ingested: int,
    error_message: str | None,
    duration_seconds: float,
) -> ScrapeLog:
    log = ScrapeLog(
        source=source,
        status=status,
        rows_ingested=rows_ingested,
        error_message=error_message,
        duration_seconds=duration_seconds,
    )

    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log
