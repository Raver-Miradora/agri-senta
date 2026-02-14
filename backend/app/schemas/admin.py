from datetime import datetime

from pydantic import BaseModel


class ScrapeTriggerResponse(BaseModel):
    status: str
    source: str
    rows_ingested: int


class ScrapeLogResponse(BaseModel):
    id: int
    source: str
    status: str
    rows_ingested: int
    error_message: str | None
    duration_seconds: float | None
    executed_at: datetime

    model_config = {"from_attributes": True}
