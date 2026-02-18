"""Tests for /api/v1/export endpoints (CSV export)."""

import csv
import io


async def test_export_prices_csv_returns_200(client):
    resp = await client.get("/api/v1/export/prices.csv")
    assert resp.status_code == 200
    assert "text/csv" in resp.headers.get("content-type", "")


async def test_export_prices_csv_has_content_disposition(client):
    resp = await client.get("/api/v1/export/prices.csv")
    cd = resp.headers.get("content-disposition", "")
    assert "attachment" in cd
    assert "prices" in cd.lower()


async def test_export_prices_csv_valid_csv(client):
    resp = await client.get("/api/v1/export/prices.csv")
    reader = csv.reader(io.StringIO(resp.text))
    rows = list(reader)
    # At least a header + 1 data row
    assert len(rows) >= 2
    header = rows[0]
    assert "commodity_name" in header or "commodity_id" in header


async def test_export_forecasts_csv_returns_200(client):
    resp = await client.get("/api/v1/export/forecasts.csv")
    assert resp.status_code == 200
    assert "text/csv" in resp.headers.get("content-type", "")


async def test_export_forecasts_csv_has_content_disposition(client):
    resp = await client.get("/api/v1/export/forecasts.csv")
    cd = resp.headers.get("content-disposition", "")
    assert "attachment" in cd
    assert "forecasts" in cd.lower()


async def test_export_forecasts_csv_valid_csv(client):
    resp = await client.get("/api/v1/export/forecasts.csv")
    reader = csv.reader(io.StringIO(resp.text))
    rows = list(reader)
    # At least a header + 1 data row (seeded_session has 7 forecasts)
    assert len(rows) >= 2
    header = rows[0]
    assert "predicted_price" in header or "commodity_id" in header
