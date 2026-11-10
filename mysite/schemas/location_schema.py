from datetime import datetime
from pydantic import BaseModel


class LocationInputSchema(BaseModel):
    courier_id: int
    latitude: float
    longitude: float


class LocationOutputSchema(BaseModel):
    id: int
    courier_id: int
    latitude: float
    longitude: float
    recorded_at: datetime
