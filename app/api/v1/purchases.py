"""Purchase API endpoints.

This module defines REST API endpoints for purchase management,
including CRUD operations and business logic for food purchases.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Query, status

from app.models.purchase import (
    Purchase,
    PurchaseCreate,
    PurchasePayload,
    PurchaseUpdate,
)
from app.api.deps import purchase_service_depends

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(prefix="/v1/purchases", tags=["purchases"])


@router.get("/", response_model=List[Purchase])
def get_purchases(
    purchase_service: purchase_service_depends, payload: PurchasePayload = Query()
) -> List[Purchase]:
    """Retrieve all purchases."""
    return purchase_service.get_purchases(payload)


@router.get("/{purchase_id}", response_model=Purchase)
def get_purchase(
    purchase_service: purchase_service_depends, purchase_id: str
) -> Purchase:
    """Retrieve a specific purchase by ID.

    Args:
        purchase_id: Unique identifier of the purchase

    Returns:
        Purchase: The requested purchase record
    """
    return purchase_service.get_purchase(purchase_id)


@router.post("/", response_model=Purchase, status_code=status.HTTP_201_CREATED)
def create_purchase_endpoint(purchase_service: purchase_service_depends, payload: PurchaseCreate) -> Purchase:
    """Create a new purchase.

    Args:
        payload: Purchase creation data including category reference

    Returns:
        Purchase: The newly created purchase
    """
    return purchase_service.create_purchase(payload)


@router.put("/{purchase_id}", response_model=Purchase)
def update_purchase_endpoint(purchase_service: purchase_service_depends, purchase_id: UUID, payload: PurchaseUpdate) -> Purchase:
    """Update an existing purchase.

    Args:
        purchase_id: Unique identifier of the purchase to update
        payload: Purchase update data (only provided fields will be updated)

    Returns:
        Purchase: The updated purchase
    """
    return purchase_service.update_purchase(purchase_id, payload)


@router.delete("/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase_endpoint(purchase_service: purchase_service_depends, purchase_id: UUID) -> None:
    """Delete a purchase.

    Args:
        purchase_id: Unique identifier of the purchase to delete
    """
    purchase_service.delete_purchase(purchase_id)
