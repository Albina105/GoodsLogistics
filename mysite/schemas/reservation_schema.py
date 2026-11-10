from datetime import datetime
from pydantic import BaseModel, Field
from mysite.database.models import ReservationStatus


class ReservationInputSchema(BaseModel):
    order_id: int
    inventory_id: int
    quantity: int = Field(ge=1)
    status: ReservationStatus = ReservationStatus.active
    expires_at: datetime


class ReservationOutputSchema(BaseModel):
    id: int
    order_id: int
    inventory_id: int
    quantity: int
    status: ReservationStatus
    expires_at: datetime
    created_at: datetime
