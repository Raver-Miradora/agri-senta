"""Tests for /api/v1/commodities endpoints."""


async def test_list_commodities_returns_200(client):
    resp = await client.get("/api/v1/commodities")
    assert resp.status_code == 200


async def test_list_commodities_returns_list(client):
    resp = await client.get("/api/v1/commodities")
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 3  # seeded 3 commodities


async def test_commodities_ordered_by_name(client):
    resp = await client.get("/api/v1/commodities")
    data = resp.json()
    names = [c["name"] for c in data]
    assert names == sorted(names)


async def test_commodity_has_required_fields(client):
    resp = await client.get("/api/v1/commodities")
    item = resp.json()[0]
    assert "id" in item
    assert "name" in item
    assert "category" in item
    assert "unit" in item
    assert "created_at" in item
