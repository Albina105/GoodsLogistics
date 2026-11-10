from datetime import datetime
from pydantic import BaseModel, Field
from mysite.database.models import WarehouseStatus


class WarehouseInputSchema(BaseModel):
    city_id: int
    code: str
    name: str
    street: str
    latitude: float
    longitude: float
    capacity: int = Field(ge=0)
    status: WarehouseStatus = WarehouseStatus.active


class WarehouseOutputSchema(BaseModel):
    id: int
    city_id: int
    code: str
    name: str
    street: str
    latitude: float
    longitude: float
    capacity: int
    status: WarehouseStatus
    created_at: datetime
