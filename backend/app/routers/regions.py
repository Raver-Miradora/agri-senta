from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.models import Region
from app.schemas import RegionResponse

router = APIRouter(prefix="/regions", tags=["Barangays"])


@router.get("", response_model=list[RegionResponse])
async def list_regions(db: AsyncSession = Depends(get_db_session)) -> list[RegionResponse]:
    result = await db.execute(select(Region).order_by(Region.name.asc()))
    return list(result.scalars().all())
