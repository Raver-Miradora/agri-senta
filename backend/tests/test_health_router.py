from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers.health import router as health_router


def test_health_endpoint_returns_ok() -> None:
    app = FastAPI()
    app.include_router(health_router, prefix="/api/v1")

    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
