"""Transformation data models.

This module defines Pydantic models for transformation entities, representing
the process of converting purchased items into prepared food items.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class TransformationBase(BaseModel):
    """Base transformation model with common fields.
    
    Attributes:
        name: Name of the transformation process
        purchase_id: Reference to the purchase being transformed
        output_quantity: Amount produced after transformation
        transformed_at: When the transformation was performed
    """
    name: str = Field(..., description="Name of the transformation process", min_length=1, max_length=200)
    purchase_id: UUID = Field(..., description="Reference to the purchase being transformed")
    output_quantity: float = Field(..., description="Amount produced after transformation", gt=0)
    transformed_at: datetime = Field(..., description="When the transformation was performed")


class TransformationCreate(TransformationBase):
    """Schema for creating a new transformation.
    
    Inherits all fields from TransformationBase.
    """
    pass


class TransformationUpdate(BaseModel):
    """Schema for updating an existing transformation.
    
    All fields are optional to allow partial updates.
    """
    name: str | None = Field(None, description="Updated transformation name", min_length=1, max_length=200)
    purchase_id: UUID | None = Field(None, description="Updated purchase reference")
    output_quantity: float | None = Field(None, description="Updated output quantity", gt=0)
    transformed_at: datetime | None = Field(None, description="Updated transformation timestamp")


class Transformation(TransformationBase):
    """Complete transformation model with database fields.
    
    Includes all base fields plus database-generated fields.
    
    Attributes:
        id: Unique transformation identifier
        created_at: Timestamp when transformation record was created
    """
    id: UUID = Field(..., description="Unique transformation identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
