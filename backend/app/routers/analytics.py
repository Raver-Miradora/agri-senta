from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.schemas.analytics import (
    CheapestRegionResponse,
    PriceSpikeResponse,
    RegionalComparisonResponse,
    RollingAverageResponse,
    SeasonalPatternResponse,
    WeeklyVarianceResponse,
)
from app.services.analytics_service import (
    get_cheapest_region,
    get_price_spikes,
    get_regional_comparison,
    get_rolling_average,
    get_seasonal_pattern,
    get_weekly_variance,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/weekly-variance", response_model=list[WeeklyVarianceResponse])
async def weekly_variance(db: AsyncSession = Depends(get_db_session)) -> list[WeeklyVarianceResponse]:
    rows = await get_weekly_variance(db)
    return [WeeklyVarianceResponse(**row) for row in rows]


@router.get("/regional-comparison", response_model=list[RegionalComparisonResponse])
async def regional_comparison(
    commodity_id: int | None = None,
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
    db: AsyncSession = Depends(get_db_session),
) -> list[RegionalComparisonResponse]:
    rows = await get_regional_comparison(
        db,
        commodity_id=commodity_id,
        from_date=from_date,
        to_date=to_date,
    )
    return [RegionalComparisonResponse(**row) for row in rows]


@router.get("/price-spikes", response_model=list[PriceSpikeResponse])
async def price_spikes(
    commodity_id: int | None = None,
    region_id: int | None = None,
    db: AsyncSession = Depends(get_db_session),
) -> list[PriceSpikeResponse]:
    rows = await get_price_spikes(db, commodity_id=commodity_id, region_id=region_id)
    return [PriceSpikeResponse(**row) for row in rows]


@router.get("/cheapest-region/{commodity_id}", response_model=CheapestRegionResponse)
async def cheapest_region(commodity_id: int, db: AsyncSession = Depends(get_db_session)) -> CheapestRegionResponse:
    row = await get_cheapest_region(db, commodity_id=commodity_id)
    if row is None:
        raise HTTPException(status_code=404, detail="No price data found for commodity")
    return CheapestRegionResponse(**row)


@router.get("/rolling-average/{commodity_id}", response_model=list[RollingAverageResponse])
async def rolling_average(
    commodity_id: int,
    region_id: int | None = None,
    db: AsyncSession = Depends(get_db_session),
) -> list[RollingAverageResponse]:
    rows = await get_rolling_average(db, commodity_id=commodity_id, region_id=region_id)
    return [RollingAverageResponse(**row) for row in rows]


@router.get("/seasonal/{commodity_id}", response_model=list[SeasonalPatternResponse])
async def seasonal_pattern(commodity_id: int, db: AsyncSession = Depends(get_db_session)) -> list[SeasonalPatternResponse]:
    rows = await get_seasonal_pattern(db, commodity_id=commodity_id)
    return [SeasonalPatternResponse(**row) for row in rows]
