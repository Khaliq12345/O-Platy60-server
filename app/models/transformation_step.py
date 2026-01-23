"""Transformation step data models.

This module defines Pydantic models for transformation step entities,
representing individual steps within a transformation process.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from app.models.shared import FilterPayload


class TransformationStepPayload(FilterPayload):
    """Filters for transformation step list endpoint"""
    pass


class TransformationStepBase(BaseModel):
    """Base transformation step model with common fields.
    
    Attributes:
        transformation_id: Reference to the parent transformation
        step_name: Name of this specific step (e.g., 'Grilled Chicken')
        portions: Number of portions produced in this step
        quantity: Quantity used/produced in this step
    """
    transformation_id: str = Field(..., description="Reference to the parent transformation")
    step_name: str = Field(..., description="Name of this specific step", min_length=1, max_length=200)
    portions: int = Field(..., description="Number of portions produced", gt=0)
    quantity: int = Field(..., description="Quantity used/produced in this step", gt=0)


class TransformationStepCreate(TransformationStepBase):
    """Schema for creating a new transformation step.
    
    Inherits all fields from TransformationStepBase.
    """
    pass


class TransformationStepUpdate(BaseModel):
    """Schema for updating an existing transformation step.
    
    All fields are optional to allow partial updates.
    """
    transformation_id: str | None = Field(None, description="Updated transformation reference")
    step_name: str | None = Field(None, description="Updated step name", min_length=1, max_length=200)
    portions: int | None = Field(None, description="Updated portions count", gt=0)
    quantity: int | None = Field(None, description="Updated quantity", gt=0)


class TransformationStep(TransformationStepBase):
    """Complete transformation step model with database fields.
    
    Includes all base fields plus database-generated fields.
    
    Attributes:
        id: Unique transformation step identifier
        created_at: Timestamp when step was created
    """
    id: str = Field(..., description="Unique transformation step identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
