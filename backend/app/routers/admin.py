from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies.auth import require_admin
from app.models import ScrapeLog
from app.schemas.admin import ScrapeLogResponse, ScrapeTriggerResponse
from app.services.pipeline_service import run_ingestion_pipeline

router = APIRouter(prefix="/admin/scrape", tags=["Admin"], dependencies=[Depends(require_admin)])


@router.post("/trigger", response_model=ScrapeTriggerResponse)
async def trigger_scrape(source: str = Query(default="DA", pattern="^(DA|PSA|da|psa)$")) -> ScrapeTriggerResponse:
    result = await run_ingestion_pipeline(source=source)
    return ScrapeTriggerResponse(**result)


@router.get("/logs", response_model=list[ScrapeLogResponse])
async def get_scrape_logs(
    limit: int = Query(default=20, ge=1, le=200),
    db: AsyncSession = Depends(get_db_session),
) -> list[ScrapeLogResponse]:
    result = await db.execute(select(ScrapeLog).order_by(ScrapeLog.executed_at.desc()).limit(limit))
    return list(result.scalars().all())
