from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.schemas.price import (
    DailyPriceResponse,
    LatestPriceResponse,
    PaginatedLatestPriceResponse,
    PriceHistoryResponse,
)
from app.services.price_service import get_daily_prices, get_latest_prices, get_price_history

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/daily", response_model=list[DailyPriceResponse])
async def list_daily_prices(
    commodity_id: int | None = None,
    region_id: int | None = None,
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
    limit: int = Query(default=200, ge=1, le=1000),
    db: AsyncSession = Depends(get_db_session),
) -> list[DailyPriceResponse]:
    return await get_daily_prices(
        db,
        commodity_id=commodity_id,
        region_id=region_id,
        from_date=from_date,
        to_date=to_date,
        limit=limit,
    )


@router.get("/latest", response_model=PaginatedLatestPriceResponse)
async def list_latest_prices(
    search: str | None = Query(default=None, max_length=100, description="Search commodity name"),
    category: str | None = Query(default=None, description="Filter by category"),
    region_id: int | None = Query(default=None, description="Filter by region ID"),
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db_session),
) -> PaginatedLatestPriceResponse:
    items, total = await get_latest_prices(
        db,
        search=search,
        category=category,
        region_id=region_id,
        limit=limit,
        offset=offset,
    )
    return PaginatedLatestPriceResponse(
        items=[LatestPriceResponse(**row) for row in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/history/{commodity_id}", response_model=list[PriceHistoryResponse])
async def price_history(
    commodity_id: int,
    region_id: int | None = None,
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
    db: AsyncSession = Depends(get_db_session),
) -> list[PriceHistoryResponse]:
    rows = await get_price_history(
        db,
        commodity_id=commodity_id,
        region_id=region_id,
        from_date=from_date,
        to_date=to_date,
    )
    return [PriceHistoryResponse(**row) for row in rows]
