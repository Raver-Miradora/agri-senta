"""Tests for /api/v1/forecast endpoints."""


async def test_forecast_summary_returns_200(client):
    resp = await client.get("/api/v1/forecast/summary")
    assert resp.status_code == 200


async def test_forecast_summary_has_category(client):
    resp = await client.get("/api/v1/forecast/summary")
    data = resp.json()
    assert isinstance(data, list)
    if data:
        assert "commodity_category" in data[0]
        assert "commodity_name" in data[0]
        assert "predicted_price" in data[0]


async def test_forecast_by_commodity_returns_200(client):
    resp = await client.get("/api/v1/forecast/1")
    assert resp.status_code == 200


async def test_forecast_by_commodity_returns_points(client):
    resp = await client.get("/api/v1/forecast/1")
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 7  # seeded 7 forecast days


async def test_forecast_by_commodity_fields(client):
    resp = await client.get("/api/v1/forecast/1")
    data = resp.json()
    if data:
        item = data[0]
        for field in (
            "commodity_id",
            "region_id",
            "forecast_date",
            "predicted_price",
            "confidence_lower",
            "confidence_upper",
            "model_used",
            "generated_at",
        ):
            assert field in item, f"Missing field: {field}"


async def test_forecast_by_commodity_with_region(client):
    resp = await client.get("/api/v1/forecast/1", params={"region_id": 1})
    data = resp.json()
    assert all(row["region_id"] == 1 for row in data)


async def test_forecast_nonexistent_commodity(client):
    resp = await client.get("/api/v1/forecast/9999")
    data = resp.json()
    assert data == []
