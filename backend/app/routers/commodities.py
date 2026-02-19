from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.models import Commodity
from app.schemas import CommodityResponse

router = APIRouter(prefix="/commodities", tags=["Commodities"])


@router.get("", response_model=list[CommodityResponse])
async def list_commodities(
    search: str | None = Query(default=None, max_length=100),
    category: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db_session),
) -> list[CommodityResponse]:
    stmt = select(Commodity)
    if search:
        stmt = stmt.where(Commodity.name.ilike(f"%{search}%"))
    if category:
        stmt = stmt.where(Commodity.category == category)
    stmt = stmt.order_by(Commodity.name.asc())
    result = await db.execute(stmt)
    return list(result.scalars().all())
