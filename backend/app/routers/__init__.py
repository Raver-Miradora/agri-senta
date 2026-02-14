from fastapi import APIRouter

from app.routers.commodities import router as commodities_router
from app.routers.health import router as health_router
from app.routers.regions import router as regions_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(commodities_router)
api_router.include_router(regions_router)
