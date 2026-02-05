"""Transformation data models."""

from datetime import date, datetime
from typing import Self
from pydantic import BaseModel, model_validator
from app.models.shared import FilterPayload


class TransformationPayload(FilterPayload):
    pass


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
    total_quantity_used: float = 0.0
    remaining_quantity: float = 0.0
    total_portions: int = 0
    total_wastes: float = 0.0
    unit: str

    @model_validator(mode="after")
    def capitalize(self) -> Self:
        if self.remaining_quantity == 0.0:
            self.remaining_quantity = self.quantity_usable
        return self


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


class TransformationSummary(Transformation):
    total_portions: int
    total_step_quantity: int
    step_count: int
    remaining_quantity: float
