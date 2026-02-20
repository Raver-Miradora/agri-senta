"""Price alerts and price monitoring endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.models.commodity import Commodity
from app.models.price_alert import PriceAlert
from app.models.region import Region

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
async def list_alerts(
    commodity_id: int | None = Query(None),
    severity: str | None = Query(None),
    unresolved_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db_session),
):
    stmt = (
        select(
            PriceAlert.id,
            PriceAlert.commodity_id,
            Commodity.name.label("commodity_name"),
            PriceAlert.region_id,
            Region.name.label("region_name"),
            PriceAlert.alert_type,
            PriceAlert.severity,
            PriceAlert.current_price,
            PriceAlert.threshold_price,
            PriceAlert.message,
            PriceAlert.triggered_at,
            PriceAlert.is_resolved,
        )
        .join(Commodity, PriceAlert.commodity_id == Commodity.id)
        .outerjoin(Region, PriceAlert.region_id == Region.id)
    )
    if commodity_id:
        stmt = stmt.where(PriceAlert.commodity_id == commodity_id)
    if severity:
        stmt = stmt.where(PriceAlert.severity == severity)
    if unresolved_only:
        stmt = stmt.where(PriceAlert.is_resolved.is_(False))
    stmt = stmt.order_by(PriceAlert.triggered_at.desc()).limit(limit)
    result = await db.execute(stmt)
    rows = result.all()
    return [
        {
            "id": r.id,
            "commodity_id": r.commodity_id,
            "commodity_name": r.commodity_name,
            "region_id": r.region_id,
            "region_name": r.region_name,
            "alert_type": r.alert_type,
            "severity": r.severity,
            "current_price": float(r.current_price) if r.current_price else 0,
            "threshold_price": float(r.threshold_price) if r.threshold_price else None,
            "message": r.message,
            "triggered_at": r.triggered_at.isoformat(),
            "is_resolved": r.is_resolved,
        }
        for r in rows
    ]
