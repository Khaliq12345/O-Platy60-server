"""Purchase API endpoints.

This module defines REST API endpoints for purchase management,
including CRUD operations and business logic for food purchases.
"""

from typing import Dict, List
from fastapi import APIRouter, Depends, Query, status

from app.models.purchase import (
    Purchase,
    PurchaseCreate,
    PurchasePayload,
    PurchaseUpdate,
    PurchaseSummary,
)
from app.api.deps import purchase_service_depends
from app.utils.auth import check_login

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(
    prefix="/v1/purchases", tags=["purchases"], dependencies=[Depends(check_login)]
)


@router.get("/", response_model=Dict[str, List[Purchase] | int])
def get_purchases(
    purchase_service: purchase_service_depends, payload: PurchasePayload = Query()
) -> Dict[str, List[Purchase] | int]:
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


@router.get("/{purchase_id}/summary", response_model=PurchaseSummary)
def get_purchase_summary(
    purchase_service: purchase_service_depends, purchase_id: str
) -> PurchaseSummary:
    """Retrieve purchase summary with transformation calculations.

    Args:
        purchase_id: Unique identifier of the purchase

    Returns:
        PurchaseSummary: Purchase with calculated transformation data
    """
    return purchase_service.purchase_summary(purchase_id)


@router.post("/", response_model=Purchase, status_code=status.HTTP_201_CREATED)
def create_purchase_endpoint(
    purchase_service: purchase_service_depends, payload: PurchaseCreate
) -> Purchase:
    """Create a new purchase.

    Args:
        payload: Purchase creation data including category reference

    Returns:
        Purchase: The newly created purchase
    """
    return purchase_service.create_purchase(payload)


@router.put("/{purchase_id}", response_model=Purchase)
def update_purchase_endpoint(
    purchase_service: purchase_service_depends,
    purchase_id: str,
    payload: PurchaseUpdate,
) -> Purchase:
    """Update an existing purchase.

    Args:
        purchase_id: Unique identifier of the purchase to update
        payload: Purchase update data (only provided fields will be updated)

    Returns:
        Purchase: The updated purchase
    """
    return purchase_service.update_purchase(purchase_id, payload)


@router.delete("/{purchase_id}")
def delete_purchase_endpoint(
    purchase_service: purchase_service_depends, purchase_id: str
) -> None:
    """Delete a purchase.

    Args:
        purchase_id: Unique identifier of the purchase to delete
    """
    purchase_service.delete_purchase(purchase_id)
