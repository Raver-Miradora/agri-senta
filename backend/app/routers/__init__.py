from fastapi import APIRouter

from app.routers.admin import router as admin_router
from app.routers.alerts import router as alerts_router
from app.routers.analytics import router as analytics_router
from app.routers.auth import router as auth_router
from app.routers.commodities import router as commodities_router
from app.routers.export import router as export_router
from app.routers.forecast import router as forecast_router
from app.routers.harvests import router as harvests_router
from app.routers.health import router as health_router
from app.routers.markets import router as markets_router
from app.routers.price_board import router as price_board_router
from app.routers.prices import router as prices_router
from app.routers.regions import router as regions_router
from app.routers.vendors import router as vendors_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(commodities_router)
api_router.include_router(regions_router)
api_router.include_router(prices_router)
api_router.include_router(price_board_router)
api_router.include_router(analytics_router)
api_router.include_router(forecast_router)
api_router.include_router(export_router)
api_router.include_router(admin_router)
api_router.include_router(vendors_router)
api_router.include_router(harvests_router)
api_router.include_router(alerts_router)
api_router.include_router(markets_router)
