from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA


@dataclass(slots=True)
class TrainedForecastModel:
    model_name: str
    linear_model: LinearRegression | None
    arima_result: object | None
    mae: float


def _train_linear_regression(prices: list[float], train_size: int) -> tuple[LinearRegression, float]:
    x_all = np.arange(len(prices), dtype=float).reshape(-1, 1)
    y_all = np.array(prices, dtype=float)

    model = LinearRegression()
    model.fit(x_all[:train_size], y_all[:train_size])

    predictions = model.predict(x_all[train_size:])
    mae = float(mean_absolute_error(y_all[train_size:], predictions))
    return model, mae


def _train_arima(prices: list[float], train_size: int) -> tuple[object, float]:
    train_values = np.array(prices[:train_size], dtype=float)
    test_values = np.array(prices[train_size:], dtype=float)

    fitted = ARIMA(train_values, order=(1, 1, 1)).fit()
    forecast = fitted.forecast(steps=len(test_values))
    mae = float(mean_absolute_error(test_values, forecast))
    return fitted, mae


def train_best_model(prices: list[float]) -> TrainedForecastModel:
    if len(prices) < 8:
        model = LinearRegression()
        x_all = np.arange(len(prices), dtype=float).reshape(-1, 1)
        y_all = np.array(prices, dtype=float)
        model.fit(x_all, y_all)
        return TrainedForecastModel(model_name="linear_regression", linear_model=model, arima_result=None, mae=0.0)

    train_size = max(5, int(len(prices) * 0.8))
    if train_size >= len(prices):
        train_size = len(prices) - 1

    linear_model, linear_mae = _train_linear_regression(prices, train_size)

    try:
        arima_result, arima_mae = _train_arima(prices, train_size)
    except Exception:
        return TrainedForecastModel(
            model_name="linear_regression",
            linear_model=linear_model,
            arima_result=None,
            mae=linear_mae,
        )

    if arima_mae <= linear_mae:
        return TrainedForecastModel(
            model_name="arima_1_1_1",
            linear_model=None,
            arima_result=arima_result,
            mae=arima_mae,
        )

    return TrainedForecastModel(
        model_name="linear_regression",
        linear_model=linear_model,
        arima_result=None,
        mae=linear_mae,
    )
