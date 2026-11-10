from datetime import datetime
from pydantic import BaseModel, Field


class InventoryInputSchema(BaseModel):
    warehouse_id: int
    product_id: int
    quantity: int = Field(default=0, ge=0)
    reserved_quantity: int = Field(default=0, ge=0)


class InventoryOutputSchema(BaseModel):
    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    reserved_quantity: int
    updated_at: datetime
