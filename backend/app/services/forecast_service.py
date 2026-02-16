import logging
from collections import defaultdict
from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.ml.predictor import generate_forecast_points
from app.ml.trainer import train_best_model
from app.models import Commodity, DailyPrice, PriceForecast, Region

logger = logging.getLogger("agrisenta.forecast")


async def _build_history_by_pair(session: AsyncSession) -> dict[tuple[int, int], list[tuple[date, float]]]:
    statement = (
        select(DailyPrice.commodity_id, DailyPrice.region_id, DailyPrice.date, DailyPrice.price_prevailing)
        .order_by(DailyPrice.commodity_id.asc(), DailyPrice.region_id.asc(), DailyPrice.date.asc())
    )
    result = await session.execute(statement)

    grouped: dict[tuple[int, int], list[tuple[date, float]]] = defaultdict(list)
    for commodity_id, region_id, row_date, price_prevailing in result.all():
        grouped[(commodity_id, region_id)].append((row_date, float(price_prevailing)))

    return grouped


async def regenerate_all_forecasts(horizon_days: int = 7) -> dict[str, int]:
    generated_rows = 0

    async with AsyncSessionLocal() as session:
        history_map = await _build_history_by_pair(session)
        logger.info("Found %d commodity-region pairs for forecasting", len(history_map))

        for (commodity_id, region_id), series in history_map.items():
            prices = [price for _, price in series]
            if len(prices) < 5:
                continue

            trained_model = train_best_model(prices)
            last_date = series[-1][0]
            points = generate_forecast_points(
                trained=trained_model,
                history=prices,
                start_date=last_date,
                horizon_days=horizon_days,
            )

            if not points:
                continue

            await session.execute(
                delete(PriceForecast).where(
                    PriceForecast.commodity_id == commodity_id,
                    PriceForecast.region_id == region_id,
                    PriceForecast.forecast_date > last_date,
                )
            )

            for point in points:
                session.add(
                    PriceForecast(
                        commodity_id=commodity_id,
                        region_id=region_id,
                        forecast_date=point["forecast_date"],
                        predicted_price=Decimal(str(round(point["predicted_price"], 2))),
                        confidence_lower=Decimal(str(round(point["confidence_lower"], 2))),
                        confidence_upper=Decimal(str(round(point["confidence_upper"], 2))),
                        model_used=trained_model.model_name,
                    )
                )
                generated_rows += 1

        await session.commit()

    return {"status": "success", "rows_generated": generated_rows}


async def get_forecast_by_commodity(session: AsyncSession, *, commodity_id: int, region_id: int | None) -> list[PriceForecast]:
    statement = select(PriceForecast).where(PriceForecast.commodity_id == commodity_id)

    if region_id is not None:
        statement = statement.where(PriceForecast.region_id == region_id)

    statement = statement.order_by(PriceForecast.region_id.asc(), PriceForecast.forecast_date.asc())
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_forecast_summary(session: AsyncSession) -> list[dict]:
    today = datetime.now(UTC).date()

    earliest_forecast_subquery = (
        select(PriceForecast.commodity_id, PriceForecast.region_id, func.min(PriceForecast.forecast_date).label("first_date"))
        .where(PriceForecast.forecast_date >= today)
        .group_by(PriceForecast.commodity_id, PriceForecast.region_id)
        .subquery()
    )

    statement = (
        select(
            PriceForecast.commodity_id,
            Commodity.name.label("commodity_name"),
            PriceForecast.region_id,
            Region.code.label("region_code"),
            PriceForecast.forecast_date,
            PriceForecast.predicted_price,
            PriceForecast.model_used,
        )
        .join(
            earliest_forecast_subquery,
            (PriceForecast.commodity_id == earliest_forecast_subquery.c.commodity_id)
            & (PriceForecast.region_id == earliest_forecast_subquery.c.region_id)
            & (PriceForecast.forecast_date == earliest_forecast_subquery.c.first_date),
        )
        .join(Commodity, Commodity.id == PriceForecast.commodity_id)
        .join(Region, Region.id == PriceForecast.region_id)
        .order_by(Commodity.name.asc(), Region.code.asc())
    )

    result = await session.execute(statement)
    return [dict(row._mapping) for row in result]
