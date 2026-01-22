"""Category data models.

This module defines Pydantic models for category entities, including
base models, creation/update schemas, and the main category model.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from app.models.shared import FilterPayload


class CategoryBase(BaseModel):
    """Base category model with common fields.
    
    Attributes:
        name: The category name (e.g., 'Vegetables', 'Meat')
    """
    name: str = Field(..., description="Category name", min_length=1, max_length=100)


class CategoryCreate(CategoryBase):
    """Schema for creating a new category.
    
    Inherits all fields from CategoryBase.
    """
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating an existing category.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        name: Updated category name
    """
    name: str | None = Field(None, description="Updated category name", min_length=1, max_length=100)


class CategoryPayload(FilterPayload):
    """Filters for category list endpoint"""
    pass


class Category(CategoryBase):
    """Complete category model with database fields.
    
    Includes all base fields plus database-generated fields.
    
    Attributes:
        id: Unique category identifier
        created_at: Timestamp when category was created
        updated_at: Timestamp when category was last updated
    """
    id: str = Field(..., description="Unique category identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
