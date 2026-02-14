from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.models import Commodity
from app.schemas import CommodityResponse

router = APIRouter(prefix="/commodities", tags=["Commodities"])


@router.get("", response_model=list[CommodityResponse])
async def list_commodities(db: AsyncSession = Depends(get_db_session)) -> list[CommodityResponse]:
    result = await db.execute(select(Commodity).order_by(Commodity.name.asc()))
    return list(result.scalars().all())
