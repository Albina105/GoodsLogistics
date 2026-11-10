from datetime import datetime
from pydantic import BaseModel
from mysite.database.models import DeliveryStatus


class TrackingInputSchema(BaseModel):
    delivery_id: int
    status: DeliveryStatus
    latitude: float
    longitude: float
    description: str


class TrackingOutputSchema(BaseModel):
    id: int
    delivery_id: int
    status: DeliveryStatus
    latitude: float
    longitude: float
    description: str
    created_at: datetime
