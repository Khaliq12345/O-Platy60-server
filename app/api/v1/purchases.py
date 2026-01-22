"""Purchase API endpoints.

This module defines REST API endpoints for purchase management,
including CRUD operations and business logic for food purchases.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status

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
    # Pass the payload (now populated from query params) to your service
    results = purchase_service.get_purchases(payload)
    return results


@router.get("/{purchase_id}", response_model=Purchase)
def get_purchase(
    purchase_service: purchase_service_depends, purchase_id: str
) -> Purchase:
    """Retrieve a specific purchase by ID.

    Args:
        purchase_id: Unique identifier of the purchase

    Returns:
        Purchase: The requested purchase record

    Raises:
        HTTPException: If purchase is not found
    """
    results = purchase_service.get_purchase(purchase_id)
    return results


#
#
# @router.post("/", response_model=Purchase, status_code=status.HTTP_201_CREATED)
# def create_purchase_endpoint(payload: PurchaseCreate) -> Purchase:
#     """Create a new purchase.
#
#     Args:
#         payload: Purchase creation data including category reference
#
#     Returns:
#         Purchase: The newly created purchase
#
#     Raises:
#         HTTPException: If referenced category doesn't exist or creation fails
#     """
#     return create_purchase(payload)
#
#
# @router.put("/{purchase_id}", response_model=Purchase)
# def update_purchase_endpoint(purchase_id: UUID, payload: PurchaseUpdate) -> Purchase:
#     """Update an existing purchase.
#
#     Args:
#         purchase_id: Unique identifier of the purchase to update
#         payload: Purchase update data (only provided fields will be updated)
#
#     Returns:
#         Purchase: The updated purchase
#
#     Raises:
#         HTTPException: If purchase or referenced category is not found
#     """
#     return update_purchase(purchase_id, payload)
#
#
# @router.delete("/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_purchase_endpoint(purchase_id: UUID) -> None:
#     """Delete a purchase.
#
#     Args:
#         purchase_id: Unique identifier of the purchase to delete
#
#     Raises:
#         HTTPException: If purchase is not found or has dependent transformations
#     """
#     get_purchase_by_id(purchase_id)  # Validate exists
#     delete_purchase(purchase_id)
#
#
# @router.get("/{purchase_id}/remaining-stock", response_model=float)
# def get_remaining_stock(purchase_id: UUID) -> float:
#     """Calculate remaining stock for a purchase.
#
#     Args:
#         purchase_id: Unique identifier of the purchase
#
#     Returns:
#         float: Remaining quantity available for transformation
#
#     Raises:
#         HTTPException: If purchase is not found
#
#     Note:
#         Currently returns the full purchase quantity as a placeholder.
#         TODO: Implement actual calculation based on transformations.
#     """
#     purchase: Purchase = get_purchase_by_id(purchase_id)
#     # TODO: Replace with real calculation based on transformations
#     return float(purchase.quantity)  # placeholder
