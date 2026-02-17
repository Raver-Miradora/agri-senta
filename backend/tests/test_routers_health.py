"""Tests for /api/v1/health endpoint."""


async def test_health_returns_200(client):
    resp = await client.get("/api/v1/health")
    assert resp.status_code == 200


async def test_health_body(client):
    resp = await client.get("/api/v1/health")
    assert resp.json() == {"status": "ok"}
