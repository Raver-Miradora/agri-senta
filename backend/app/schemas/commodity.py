from datetime import datetime

from pydantic import BaseModel


class CommodityResponse(BaseModel):
    id: int
    name: str
    category: str
    unit: str
    image_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
