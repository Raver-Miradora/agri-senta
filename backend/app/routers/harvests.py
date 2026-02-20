"""Harvest record endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies.auth import require_admin
from app.models.commodity import Commodity
from app.models.harvest_record import HarvestRecord
from app.models.region import Region
from app.schemas.harvest import HarvestRecordCreate, HarvestSummaryResponse

router = APIRouter(prefix="/harvests", tags=["harvests"])


@router.get("")
async def list_harvests(
    region_id: int | None = Query(None),
    commodity_id: int | None = Query(None),
    season: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db_session),
):
    stmt = (
        select(
            HarvestRecord.id,
            HarvestRecord.region_id,
            Region.name.label("region_name"),
            HarvestRecord.commodity_id,
            Commodity.name.label("commodity_name"),
            HarvestRecord.quantity_kg,
            HarvestRecord.area_hectares,
            HarvestRecord.season,
            HarvestRecord.harvest_date,
            HarvestRecord.farmer_name,
            HarvestRecord.notes,
        )
        .join(Region, HarvestRecord.region_id == Region.id)
        .join(Commodity, HarvestRecord.commodity_id == Commodity.id)
    )
    if region_id:
        stmt = stmt.where(HarvestRecord.region_id == region_id)
    if commodity_id:
        stmt = stmt.where(HarvestRecord.commodity_id == commodity_id)
    if season:
        stmt = stmt.where(HarvestRecord.season == season)
    stmt = stmt.order_by(HarvestRecord.harvest_date.desc()).limit(limit).offset(offset)
    result = await db.execute(stmt)
    rows = result.all()
    return [
        {
            "id": r.id,
            "region_id": r.region_id,
            "region_name": r.region_name,
            "commodity_id": r.commodity_id,
            "commodity_name": r.commodity_name,
            "quantity_kg": float(r.quantity_kg),
            "area_hectares": float(r.area_hectares) if r.area_hectares else None,
            "season": r.season,
            "harvest_date": str(r.harvest_date),
            "farmer_name": r.farmer_name,
            "notes": r.notes,
        }
        for r in rows
    ]


@router.get("/summary", response_model=list[HarvestSummaryResponse])
async def harvest_summary(
    season: str | None = Query(None),
    db: AsyncSession = Depends(get_db_session),
):
    """Aggregate harvest totals grouped by commodity + season."""
    stmt = (
        select(
            HarvestRecord.commodity_id,
            Commodity.name.label("commodity_name"),
            HarvestRecord.season,
            func.sum(HarvestRecord.quantity_kg).label("total_kg"),
            func.sum(HarvestRecord.area_hectares).label("total_hectares"),
            func.count(HarvestRecord.id).label("record_count"),
        )
        .join(Commodity, HarvestRecord.commodity_id == Commodity.id)
        .group_by(HarvestRecord.commodity_id, Commodity.name, HarvestRecord.season)
    )
    if season:
        stmt = stmt.where(HarvestRecord.season == season)
    stmt = stmt.order_by(func.sum(HarvestRecord.quantity_kg).desc())
    result = await db.execute(stmt)
    rows = result.all()
    return [
        HarvestSummaryResponse(
            commodity_id=r.commodity_id,
            commodity_name=r.commodity_name,
            season=r.season,
            total_kg=float(r.total_kg) if r.total_kg else 0,
            total_hectares=float(r.total_hectares) if r.total_hectares else None,
            record_count=r.record_count,
        )
        for r in rows
    ]


@router.post("", status_code=201)
async def create_harvest(
    payload: HarvestRecordCreate,
    _admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db_session),
):
    record = HarvestRecord(**payload.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return {"id": record.id, "message": "Harvest record created"}


@router.delete("/{harvest_id}", status_code=204)
async def delete_harvest(
    harvest_id: int,
    _admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db_session),
):
    result = await db.execute(select(HarvestRecord).where(HarvestRecord.id == harvest_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(404, "Harvest record not found")
    await db.delete(record)
    await db.commit()
