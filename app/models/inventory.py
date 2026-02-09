from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InventoryBase(BaseModel):
    name: str
    initial_quantity: int
    unit: str
    category: Optional[str] = None


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    initial_quantity: Optional[float] = None
    unit: Optional[str] = None
    category: Optional[str] = None


class InventoryResponse(InventoryBase):
    inventory_id: str
    created_at: datetime
