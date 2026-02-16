"""Purchase data models."""

from datetime import date, datetime
from typing import List

from pydantic import BaseModel

from app.models.shared import FilterPayload
from app.models.transformation import Transformation


class PurchasePayload(FilterPayload):
    category_id: str | None = None
    created_by: str | None = None


class PurchaseBase(BaseModel):
    item_name: str
    quantity: float
    unit: str
    price_per_unit: float
    total_price: float
    purchase_date: date
    category_id: str
    inventory_id: str
    notes: str | None = None


class PurchaseCreate(PurchaseBase):
    created_by: str


class Purchase(PurchaseBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    transformations: List[Transformation] | None = None

    class Config:
        from_attributes = True
