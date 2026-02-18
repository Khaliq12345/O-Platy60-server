"""Ingredient models.
This module defines Pydantic models for ingredient data validation,
serialization, and API request/response schemas.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Measurement(str, Enum):
    """Measurement units for ingredients."""

    KG = "kg"
    G = "g"
    L = "l"
    ML = "ml"
    UNIT = "unit"
    TSP = "tsp"
    TBSP = "tbsp"


class IngredientBase(BaseModel):
    name: str
    unit: Measurement
    category: Optional[UUID] = None
    total_quantity: Optional[float] = None


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    name: str | None = None
    unit: Measurement | None = None
    category: UUID | None = None
    total_quantity: float | None = None


class Ingredient(IngredientBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class IngredientPayload(BaseModel):
    """Query parameters for listing ingredients."""

    limit: int = 10
    offset: int = 0
    name: Optional[str] = None
    category: Optional[UUID] = None
