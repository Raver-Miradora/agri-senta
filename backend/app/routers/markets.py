"""Markets listing endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.models.market import Market
from app.schemas.market import MarketResponse

router = APIRouter(prefix="/markets", tags=["markets"])


@router.get("", response_model=list[MarketResponse])
async def list_markets(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Market).order_by(Market.name))
    return result.scalars().all()
