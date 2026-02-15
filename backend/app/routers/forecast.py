from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.schemas.forecast import ForecastPointResponse, ForecastSummaryResponse
from app.services.forecast_service import get_forecast_by_commodity, get_forecast_summary

router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get("/summary", response_model=list[ForecastSummaryResponse])
async def forecast_summary(db: AsyncSession = Depends(get_db_session)) -> list[ForecastSummaryResponse]:
    rows = await get_forecast_summary(db)
    return [ForecastSummaryResponse(**row) for row in rows]


@router.get("/{commodity_id}", response_model=list[ForecastPointResponse])
async def forecast_by_commodity(
    commodity_id: int,
    region_id: int | None = None,
    db: AsyncSession = Depends(get_db_session),
) -> list[ForecastPointResponse]:
    rows = await get_forecast_by_commodity(db, commodity_id=commodity_id, region_id=region_id)
    return [ForecastPointResponse.model_validate(row) for row in rows]
