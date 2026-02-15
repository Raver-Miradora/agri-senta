from datetime import date

from app.ml.predictor import generate_forecast_points
from app.ml.trainer import train_best_model


def test_train_best_model_returns_supported_model_name() -> None:
    prices = [45.0, 45.8, 46.3, 46.7, 47.1, 47.9, 48.4, 49.0, 49.2, 49.6]
    trained = train_best_model(prices)

    assert trained.model_name in {"linear_regression", "arima_1_1_1"}


def test_generate_forecast_points_returns_horizon_rows() -> None:
    prices = [120.0, 121.2, 122.1, 123.0, 123.4, 124.1, 124.8, 125.2]
    trained = train_best_model(prices)

    rows = generate_forecast_points(trained=trained, history=prices, start_date=date(2026, 1, 10), horizon_days=7)

    assert len(rows) == 7
    assert rows[0]["forecast_date"].isoformat() == "2026-01-11"
    assert "predicted_price" in rows[0]
