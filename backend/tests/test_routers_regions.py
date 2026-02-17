"""Tests for /api/v1/regions endpoints."""


async def test_list_regions_returns_200(client):
    resp = await client.get("/api/v1/regions")
    assert resp.status_code == 200


async def test_list_regions_returns_all_seeded(client):
    resp = await client.get("/api/v1/regions")
    data = resp.json()
    assert len(data) == 2  # seeded NCR + R03


async def test_regions_ordered_by_name(client):
    resp = await client.get("/api/v1/regions")
    data = resp.json()
    names = [r["name"] for r in data]
    assert names == sorted(names)


async def test_region_has_required_fields(client):
    resp = await client.get("/api/v1/regions")
    item = resp.json()[0]
    for field in ("id", "name", "code", "island_group", "created_at"):
        assert field in item, f"Missing field: {field}"
