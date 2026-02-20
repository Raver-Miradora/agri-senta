"""Public price board endpoint — today's market prices for broadcasting."""

from collections import defaultdict

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.models.commodity import Commodity
from app.models.daily_price import DailyPrice
from app.models.market import Market
from app.models.region import Region

router = APIRouter(prefix="/price-board", tags=["price-board"])


@router.get("")
async def get_price_board(
    market_id: int | None = Query(None, description="Filter by specific market"),
    category: str | None = Query(None),
    db: AsyncSession = Depends(get_db_session),
):
    """Today's prices grouped by category for public broadcasting."""
    # Get the two most recent dates with price data (for change %)
    dates_q = select(DailyPrice.date).distinct().order_by(DailyPrice.date.desc()).limit(2)
    dates_result = await db.execute(dates_q)
    dates = [r[0] for r in dates_result.all()]
    if not dates:
        return []

    latest_date = dates[0]
    prev_date = dates[1] if len(dates) > 1 else None

    # Latest prices (avg per commodity)
    stmt = (
        select(
            Commodity.id.label("commodity_id"),
            Commodity.name.label("commodity_name"),
            Commodity.category,
            Commodity.unit,
            func.avg(DailyPrice.price_prevailing).label("avg_price"),
        )
        .join(Commodity, DailyPrice.commodity_id == Commodity.id)
        .where(DailyPrice.date == latest_date)
        .group_by(Commodity.id, Commodity.name, Commodity.category, Commodity.unit)
    )
    if market_id:
        stmt = stmt.join(Market, DailyPrice.market_id == Market.id).where(Market.id == market_id)
    if category:
        stmt = stmt.where(Commodity.category == category)
    stmt = stmt.order_by(Commodity.category, Commodity.name)
    result = await db.execute(stmt)
    latest_rows = result.all()

    # Previous day prices for change calculation
    prev_map: dict[int, float] = {}
    if prev_date:
        prev_stmt = (
            select(
                Commodity.id.label("commodity_id"),
                func.avg(DailyPrice.price_prevailing).label("avg_price"),
            )
            .join(Commodity, DailyPrice.commodity_id == Commodity.id)
            .where(DailyPrice.date == prev_date)
            .group_by(Commodity.id)
        )
        prev_result = await db.execute(prev_stmt)
        for r in prev_result.all():
            prev_map[r.commodity_id] = float(r.avg_price)

    # Group by category
    groups: dict[str, list] = defaultdict(list)
    for r in latest_rows:
        avg = float(r.avg_price)
        prev = prev_map.get(r.commodity_id)
        change = round((avg - prev) / prev * 100, 1) if prev and prev > 0 else None
        groups[r.category].append({
            "commodity_id": r.commodity_id,
            "commodity_name": r.commodity_name,
            "unit": r.unit,
            "avg_price": round(avg, 2),
            "prev_price": round(prev, 2) if prev else None,
            "change_percent": change,
        })

    return [{"category": cat, "items": items} for cat, items in groups.items()]
