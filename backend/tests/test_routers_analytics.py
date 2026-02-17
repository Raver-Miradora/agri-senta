"""Tests for /api/v1/analytics endpoints.

Note: Some analytics queries use PostgreSQL-specific aggregate window
functions (e.g. stddev_samp, date_trunc) that are unavailable in SQLite.
Those tests are marked with ``pytest.mark.xfail`` when running against
the in-memory SQLite test database.
"""

import pytest

# --- Weekly variance uses date_trunc (PostgreSQL only) ---


@pytest.mark.xfail(reason="date_trunc not available in SQLite", strict=False)
async def test_weekly_variance_returns_200(client):
    resp = await client.get("/api/v1/analytics/weekly-variance")
    assert resp.status_code == 200


@pytest.mark.xfail(reason="date_trunc not available in SQLite", strict=False)
async def test_weekly_variance_is_list(client):
    resp = await client.get("/api/v1/analytics/weekly-variance")
    data = resp.json()
    assert isinstance(data, list)


async def test_regional_comparison_returns_200(client):
    resp = await client.get("/api/v1/analytics/regional-comparison")
    assert resp.status_code == 200


async def test_regional_comparison_filter_commodity(client):
    resp = await client.get("/api/v1/analytics/regional-comparison", params={"commodity_id": 1})
    data = resp.json()
    assert isinstance(data, list)


# --- Price spikes uses stddev_samp (PostgreSQL only) ---


@pytest.mark.xfail(reason="stddev_samp not available in SQLite", strict=False)
async def test_price_spikes_returns_200(client):
    resp = await client.get("/api/v1/analytics/price-spikes")
    assert resp.status_code == 200


@pytest.mark.xfail(reason="stddev_samp not available in SQLite", strict=False)
async def test_price_spikes_filter_commodity(client):
    resp = await client.get("/api/v1/analytics/price-spikes", params={"commodity_id": 1})
    data = resp.json()
    assert isinstance(data, list)


@pytest.mark.xfail(reason="stddev_samp not available in SQLite", strict=False)
async def test_price_spikes_filter_region(client):
    resp = await client.get("/api/v1/analytics/price-spikes", params={"region_id": 1})
    data = resp.json()
    assert isinstance(data, list)


async def test_cheapest_region_returns_200(client):
    resp = await client.get("/api/v1/analytics/cheapest-region/1")
    assert resp.status_code == 200


async def test_cheapest_region_has_fields(client):
    resp = await client.get("/api/v1/analytics/cheapest-region/1")
    data = resp.json()
    for field in ("commodity_id", "commodity_name", "region_id", "region_name", "avg_price"):
        assert field in data, f"Missing field: {field}"


async def test_cheapest_region_404_for_unknown(client):
    resp = await client.get("/api/v1/analytics/cheapest-region/9999")
    assert resp.status_code == 404


async def test_rolling_average_returns_200(client):
    resp = await client.get("/api/v1/analytics/rolling-average/1")
    assert resp.status_code == 200


async def test_rolling_average_is_list(client):
    resp = await client.get("/api/v1/analytics/rolling-average/1")
    data = resp.json()
    assert isinstance(data, list)
    if data:
        assert "date" in data[0]
        assert "avg_price" in data[0]


async def test_seasonal_pattern_returns_200(client):
    resp = await client.get("/api/v1/analytics/seasonal/1")
    assert resp.status_code == 200


async def test_seasonal_pattern_is_list(client):
    resp = await client.get("/api/v1/analytics/seasonal/1")
    data = resp.json()
    assert isinstance(data, list)
    if data:
        assert "month" in data[0]
        assert "avg_price" in data[0]
