"""Purchase data models."""

from datetime import date, datetime
from pydantic import BaseModel
from app.models.shared import FilterPayload


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
    notes: str | None = None


class PurchaseCreate(PurchaseBase):
    created_by: str


class PurchaseUpdate(BaseModel):
    # TODO: Need to be checked, all fields cannot be editable for logcal reasons
    item_name: str | None = None
    quantity: float | None = None
    unit: str | None = None
    price_per_unit: float | None = None
    total_price: float | None = None
    purchase_date: date | None = None
    category_id: str | None = None
    notes: str | None = None


class Purchase(PurchaseBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True