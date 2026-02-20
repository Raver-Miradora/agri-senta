"""Vendor management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.dependencies.auth import require_admin
from app.models.market import Market
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate

router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.get("")
async def list_vendors(
    market_id: int | None = Query(None),
    commodity_type: str | None = Query(None),
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db_session),
):
    stmt = (
        select(
            Vendor.id,
            Vendor.name,
            Vendor.stall_number,
            Vendor.market_id,
            Market.name.label("market_name"),
            Vendor.commodity_type,
            Vendor.contact_number,
            Vendor.is_active,
        )
        .outerjoin(Market, Vendor.market_id == Market.id)
    )
    if market_id:
        stmt = stmt.where(Vendor.market_id == market_id)
    if commodity_type:
        stmt = stmt.where(Vendor.commodity_type == commodity_type)
    if active_only:
        stmt = stmt.where(Vendor.is_active.is_(True))
    stmt = stmt.order_by(Vendor.name)
    result = await db.execute(stmt)
    rows = result.all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "stall_number": r.stall_number,
            "market_id": r.market_id,
            "market_name": r.market_name,
            "commodity_type": r.commodity_type,
            "contact_number": r.contact_number,
            "is_active": r.is_active,
        }
        for r in rows
    ]


@router.post("", status_code=201)
async def create_vendor(
    payload: VendorCreate,
    _admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db_session),
):
    vendor = Vendor(**payload.model_dump())
    db.add(vendor)
    await db.commit()
    await db.refresh(vendor)
    return {"id": vendor.id, "name": vendor.name, "message": "Vendor created"}


@router.delete("/{vendor_id}", status_code=204)
async def delete_vendor(
    vendor_id: int,
    _admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db_session),
):
    result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
    vendor = result.scalar_one_or_none()
    if not vendor:
        raise HTTPException(404, "Vendor not found")
    await db.delete(vendor)
    await db.commit()
