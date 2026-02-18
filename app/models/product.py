"""Product models."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.ingredients import Measurement, Ingredient


class ProductBase(BaseModel):
    name: str
    initial_portion: float
    unit: Measurement
    category: Optional[UUID] = None
    ingredient_id: UUID


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    initial_portion: float | None = None
    unit: Measurement | None = None
    category: UUID | None = None


class Product(ProductBase):
    product_id: UUID
    created_at: datetime
    ingredients: Optional[Ingredient] = None

    class Config:
        from_attributes = True


class ProductPayload(BaseModel):
    """Query parameters for listing products."""

    limit: int = 10
    offset: int = 0
    name: str | None = None
    category: UUID | None = None
    ingredient_id: UUID | None = None
