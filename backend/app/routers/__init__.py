from fastapi import APIRouter

from app.routers.admin import router as admin_router
from app.routers.analytics import router as analytics_router
from app.routers.auth import router as auth_router
from app.routers.commodities import router as commodities_router
from app.routers.forecast import router as forecast_router
from app.routers.health import router as health_router
from app.routers.prices import router as prices_router
from app.routers.regions import router as regions_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(commodities_router)
api_router.include_router(regions_router)
api_router.include_router(prices_router)
api_router.include_router(analytics_router)
api_router.include_router(forecast_router)
api_router.include_router(admin_router)
