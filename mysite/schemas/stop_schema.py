from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from mysite.database.models import StopType, StopStatus


class StopInputSchema(BaseModel):
    route_id: int
    delivery_id: int
    stop_type: StopType
    sequence: int = Field(ge=1)
    latitude: float
    longitude: float
    status: StopStatus = StopStatus.pending
    arrived_at: Optional[datetime] = None


class StopOutputSchema(BaseModel):
    id: int
    route_id: int
    delivery_id: int
    stop_type: StopType
    sequence: int
    latitude: float
    longitude: float
    status: StopStatus
    arrived_at: Optional[datetime]
