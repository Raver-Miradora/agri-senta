from datetime import date, timedelta

import numpy as np

from app.ml.trainer import TrainedForecastModel


def generate_forecast_points(
    trained: TrainedForecastModel,
    history: list[float],
    start_date: date,
    horizon_days: int = 7,
) -> list[dict]:
    if not history:
        return []

    if trained.model_name.startswith("arima") and trained.arima_result is not None:
        forecast_values = list(trained.arima_result.forecast(steps=horizon_days))
        residual_std = float(np.std(trained.arima_result.resid)) if hasattr(trained.arima_result, "resid") else 0.0
    else:
        if trained.linear_model is None:
            return []
        start_index = len(history)
        x_future = np.arange(start_index, start_index + horizon_days, dtype=float).reshape(-1, 1)
        forecast_values = list(trained.linear_model.predict(x_future))
        residual_std = float(np.std(np.array(history, dtype=float))) * 0.1

    z_value = 1.645
    lower_offset = z_value * residual_std
    upper_offset = z_value * residual_std

    rows: list[dict] = []
    for index, value in enumerate(forecast_values, start=1):
        day = start_date + timedelta(days=index)
        rows.append(
            {
                "forecast_date": day,
                "predicted_price": float(value),
                "confidence_lower": float(value - lower_offset),
                "confidence_upper": float(value + upper_offset),
            }
        )

    return rows
