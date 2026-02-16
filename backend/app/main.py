import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import AsyncSessionLocal, engine
from app.models.base import Base
from app.routers import api_router
from app.scraping.scheduler import create_scheduler
from app.services.forecast_service import regenerate_all_forecasts
from app.utils.seed_data import seed_reference_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("agrisenta")

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler = create_scheduler()

    logger.info("Creating database tables …")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    logger.info("Seeding reference data …")
    async with AsyncSessionLocal() as session:
        await seed_reference_data(session)

    logger.info("Generating initial forecasts …")
    result = await regenerate_all_forecasts(horizon_days=7)
    logger.info("Forecasts generated: %s rows", result.get("rows_generated", 0))

    scheduler.start()
    logger.info("Scheduler started")

    yield

    scheduler.shutdown(wait=False)
    logger.info("Scheduler shut down")


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
