"""Transformation step data models."""

from datetime import datetime
from pydantic import BaseModel
from app.models.shared import FilterPayload


class TransformationStepPayload(FilterPayload):
    pass


class TransformationStepBase(BaseModel):
    product_id: str
    transformation_id: str
    step_name: str
    portions: int
    quantity: int | float


class TransformationStepCreate(TransformationStepBase):
    pass


class TransformationStepUpdate(BaseModel):
    transformation_id: str | None = None
    step_name: str | None = None
    portions: int | None = None
    quantity: int | float | None = None


class TransformationStep(TransformationStepBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
