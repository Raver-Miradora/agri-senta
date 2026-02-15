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

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler = create_scheduler()

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await seed_reference_data(session)

    await regenerate_all_forecasts(horizon_days=7)

    scheduler.start()

    yield

    scheduler.shutdown(wait=False)


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
