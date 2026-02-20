"""CSV export router – streams CSV data for prices and forecasts."""

import csv
import io

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.services.forecast_service import get_forecast_summary
from app.services.price_service import get_latest_prices

router = APIRouter(prefix="/export", tags=["Export"])


def _csv_streaming_response(rows: list[dict], filename: str) -> StreamingResponse:
    """Build a StreamingResponse from a list of dicts."""
    if not rows:
        output = io.StringIO("No data available\n")
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/prices.csv")
async def export_prices_csv(
    db: AsyncSession = Depends(get_db_session),
) -> StreamingResponse:
    items, _total = await get_latest_prices(db, limit=100_000, offset=0)
    data = [dict(row) if not isinstance(row, dict) else row for row in items]
    return _csv_streaming_response(data, "agrisenta-prices.csv")


@router.get("/forecasts.csv")
async def export_forecasts_csv(
    db: AsyncSession = Depends(get_db_session),
) -> StreamingResponse:
    rows = await get_forecast_summary(db)
    data = [dict(row) if not isinstance(row, dict) else row for row in rows]
    return _csv_streaming_response(data, "agrisenta-forecasts.csv")
