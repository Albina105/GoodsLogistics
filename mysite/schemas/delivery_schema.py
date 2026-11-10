from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from mysite.database.models import DeliveryStatus


class DeliveryInputSchema(BaseModel):
    order_id: int
    warehouse_id: int
    courier_id: Optional[int] = None
    tracking_code: str
    status: DeliveryStatus = DeliveryStatus.created
    destination_address: str
    destination_latitude: float
    destination_longitude: float
    estimated_delivery_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None


class DeliveryOutputSchema(BaseModel):
    id: int
    order_id: int
    warehouse_id: int
    courier_id: Optional[int]
    tracking_code: str
    status: DeliveryStatus
    destination_address: str
    destination_latitude: float
    destination_longitude: float
    estimated_delivery_at: Optional[datetime]
    delivered_at: Optional[datetime]
    created_at: datetime
