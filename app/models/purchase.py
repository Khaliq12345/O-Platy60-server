"""Purchase data models.

This module defines Pydantic models for purchase entities, representing
food items bought by users with pricing and categorization information.
"""

from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, Field
from decimal import Decimal
from app.models.shared import FilterPayload


class PurchasePayload(FilterPayload):
    """The filters for the purchase table"""

    category_id: str | None = None


class PurchaseBase(BaseModel):
    """Base purchase model with common fields.

    Attributes:
        item_name: Name of the purchased item
        quantity: Amount purchased
        unit: Unit of measurement (e.g., 'kg', 'liters', 'pieces')
        price_per_unit: Cost per unit
        total_price: Total cost of the purchase
        purchase_date: Date when the item was purchased
        category_id: Reference to the category this item belongs to
        notes: Optional additional notes about the purchase
    """

    item_name: str = Field(
        ..., description="Name of the purchased item", min_length=1, max_length=200
    )
    quantity: float = Field(..., description="Amount purchased", gt=0)
    unit: str = Field(
        ..., description="Unit of measurement", min_length=1, max_length=50
    )
    price_per_unit: float = Field(..., description="Cost per unit", ge=0)
    total_price: float = Field(..., description="Total cost of the purchase", ge=0)
    purchase_date: date = Field(..., description="Date when the item was purchased")
    category_id: UUID = Field(..., description="Reference to the category")
    notes: str | None = Field(None, description="Optional notes", max_length=1000)


class PurchaseCreate(PurchaseBase):
    """Schema for creating a new purchase.

    Includes all base fields plus the user who created the purchase.

    Attributes:
        created_by: UUID of the user creating the purchase
    """

    created_by: UUID = Field(..., description="UUID of the user creating the purchase")


class PurchaseUpdate(BaseModel):
    """Schema for updating an existing purchase.

    All fields are optional to allow partial updates.
    """

    item_name: str | None = Field(
        None, description="Updated item name", min_length=1, max_length=200
    )
    quantity: float | None = Field(None, description="Updated quantity", gt=0)
    unit: str | None = Field(
        None, description="Updated unit", min_length=1, max_length=50
    )
    price_per_unit: float | None = Field(
        None, description="Updated price per unit", ge=0
    )
    total_price: float | None = Field(None, description="Updated total price", ge=0)
    purchase_date: date | None = Field(None, description="Updated purchase date")
    category_id: UUID | None = Field(None, description="Updated category reference")
    notes: str | None = Field(None, description="Updated notes", max_length=1000)


class Purchase(PurchaseBase):
    """Complete purchase model with database fields.

    Includes all base fields plus database-generated fields.

    Attributes:
        id: Unique purchase identifier
        created_by: UUID of the user who created the purchase
        created_at: Timestamp when purchase was created
        updated_at: Timestamp when purchase was last updated
    """

    id: UUID = Field(..., description="Unique purchase identifier")
    created_by: UUID = Field(
        ..., description="UUID of the user who created the purchase"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True
