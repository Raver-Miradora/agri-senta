from pydantic import BaseModel


class MarketResponse(BaseModel):
    id: int
    name: str
    region_id: int
    type: str
    address: str | None

    model_config = {"from_attributes": True}
