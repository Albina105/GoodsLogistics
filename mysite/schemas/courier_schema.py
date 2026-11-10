from datetime import datetime
from pydantic import BaseModel, Field
from mysite.database.models import TransportType, CourierStatus


class CourierInputSchema(BaseModel):
    user_id: int
    warehouse_id: int
    transport_type: TransportType
    status: CourierStatus = CourierStatus.offline
    max_active_orders: int = Field(default=3, ge=1)


class CourierOutputSchema(BaseModel):
    id: int
    user_id: int
    warehouse_id: int
    transport_type: TransportType
    status: CourierStatus
    max_active_orders: int
    created_at: datetime
