"""Category data models."""

from datetime import datetime
from pydantic import BaseModel
from app.models.shared import FilterPayload


class CategoryPayload(FilterPayload):
    pass


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None


class Category(CategoryBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True