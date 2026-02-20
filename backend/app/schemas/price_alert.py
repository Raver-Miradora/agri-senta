from datetime import datetime

from pydantic import BaseModel


class PriceAlertResponse(BaseModel):
    id: int
    commodity_id: int
    region_id: int | None
    alert_type: str
    severity: str
    current_price: float | None
    threshold_price: float | None
    message: str
    triggered_at: datetime
    is_resolved: bool
    created_at: datetime

    model_config = {"from_attributes": True}
