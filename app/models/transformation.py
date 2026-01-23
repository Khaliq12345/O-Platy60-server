"""Transformation data models."""

from datetime import date, datetime
from pydantic import BaseModel


class TransformationBase(BaseModel):
    purchase_id: str
    product_name: str
    quantity_received: float
    quantity_usable: float
    waste_quantity: float
    transformation_date: date
    notes: str | None = None
    cook_signature: str | None = None
    manager_signature: str | None = None


class TransformationCreate(TransformationBase):
    created_by: str


class TransformationUpdate(BaseModel):
    purchase_id: str | None = None
    product_name: str | None = None
    quantity_received: float | None = None
    quantity_usable: float | None = None
    waste_quantity: float | None = None
    transformation_date: date | None = None
    notes: str | None = None
    cook_signature: str | None = None
    manager_signature: str | None = None


class Transformation(TransformationBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True