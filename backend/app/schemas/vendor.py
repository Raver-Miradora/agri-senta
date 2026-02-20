from datetime import date, datetime

from pydantic import BaseModel


class VendorCreate(BaseModel):
    name: str
    stall_number: str | None = None
    market_id: int | None = None
    commodity_type: str | None = None
    contact_number: str | None = None
    is_active: bool = True


class VendorResponse(BaseModel):
    id: int
    name: str
    stall_number: str | None
    market_id: int
    commodity_type: str
    contact_number: str | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
