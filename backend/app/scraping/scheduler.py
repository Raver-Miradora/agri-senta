from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import get_settings
from app.services.forecast_service import regenerate_all_forecasts
from app.services.pipeline_service import run_ingestion_pipeline

settings = get_settings()


def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Asia/Manila")

    scheduler.add_job(
        run_ingestion_pipeline,
        CronTrigger.from_crontab(settings.scrape_schedule_cron),
        kwargs={"source": "DA"},
        id="daily-da-scrape",
        replace_existing=True,
    )

    scheduler.add_job(
        regenerate_all_forecasts,
        CronTrigger.from_crontab(settings.forecast_schedule_cron),
        kwargs={"horizon_days": 7},
        id="weekly-forecast-regeneration",
        replace_existing=True,
    )

    return scheduler
