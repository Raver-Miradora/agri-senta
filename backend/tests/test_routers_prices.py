"""Tests for /api/v1/prices endpoints."""


async def test_daily_prices_returns_200(client):
    resp = await client.get("/api/v1/prices/daily")
    assert resp.status_code == 200


async def test_daily_prices_default_limit(client):
    resp = await client.get("/api/v1/prices/daily")
    data = resp.json()
    # We seeded 50 daily prices total; default limit is 200 so all returned
    assert isinstance(data, list)
    assert len(data) <= 200


async def test_daily_prices_filter_by_commodity(client):
    resp = await client.get("/api/v1/prices/daily", params={"commodity_id": 1})
    data = resp.json()
    assert all(row["commodity_id"] == 1 for row in data)


async def test_daily_prices_filter_by_region(client):
    resp = await client.get("/api/v1/prices/daily", params={"region_id": 1})
    data = resp.json()
    assert all(row["region_id"] == 1 for row in data)


async def test_daily_prices_custom_limit(client):
    resp = await client.get("/api/v1/prices/daily", params={"limit": 5})
    data = resp.json()
    assert len(data) <= 5


async def test_daily_prices_limit_validation(client):
    resp = await client.get("/api/v1/prices/daily", params={"limit": 0})
    assert resp.status_code == 422  # below ge=1


async def test_latest_prices_returns_200(client):
    resp = await client.get("/api/v1/prices/latest")
    assert resp.status_code == 200


async def test_latest_prices_has_category(client):
    resp = await client.get("/api/v1/prices/latest")
    data = resp.json()
    assert len(data) > 0
    assert "commodity_category" in data[0]


async def test_latest_prices_fields(client):
    resp = await client.get("/api/v1/prices/latest")
    data = resp.json()
    if data:
        item = data[0]
        for field in ("commodity_id", "commodity_name", "region_id", "region_code", "date", "avg_price"):
            assert field in item, f"Missing field: {field}"


async def test_price_history_returns_200(client):
    resp = await client.get("/api/v1/prices/history/1")
    assert resp.status_code == 200


async def test_price_history_returns_data(client):
    resp = await client.get("/api/v1/prices/history/1")
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0


async def test_price_history_with_region_filter(client):
    resp = await client.get("/api/v1/prices/history/1", params={"region_id": 1})
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0


async def test_price_history_nonexistent_commodity(client):
    resp = await client.get("/api/v1/prices/history/9999")
    data = resp.json()
    assert data == []
