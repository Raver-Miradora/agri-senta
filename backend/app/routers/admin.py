from fastapi import APIRouter, Query
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import ScrapeLog
from app.schemas.admin import ScrapeLogResponse, ScrapeTriggerResponse
from app.services.pipeline_service import run_ingestion_pipeline

router = APIRouter(prefix="/admin/scrape", tags=["Admin"])


@router.post("/trigger", response_model=ScrapeTriggerResponse)
async def trigger_scrape(source: str = Query(default="DA", pattern="^(DA|PSA|da|psa)$")) -> ScrapeTriggerResponse:
    result = await run_ingestion_pipeline(source=source)
    return ScrapeTriggerResponse(**result)


@router.get("/logs", response_model=list[ScrapeLogResponse])
async def get_scrape_logs(limit: int = 20) -> list[ScrapeLogResponse]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ScrapeLog).order_by(ScrapeLog.executed_at.desc()).limit(limit))
        return list(result.scalars().all())
