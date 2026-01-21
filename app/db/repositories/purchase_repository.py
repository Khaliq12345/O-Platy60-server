"""Purchase repository for database operations.

This module provides data access layer functions for purchase entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List
from uuid import UUID
from supabase import Client
from fastapi import HTTPException, status
from app.db.supabase import get_supabase
from app.services.serialization import serialize_for_supabase
from app.models.purchase import Purchase, PurchaseCreate, PurchaseUpdate


# Database table name for purchases
TABLE_NAME: str = "purchases"


def list_purchases() -> List[Purchase]:
    """Retrieve all purchases from the database.
    
    Returns:
        List[Purchase]: List of all purchase records ordered by date (newest first)
        
    Raises:
        HTTPException: If database operation fails
    """
    client: Client = get_supabase()
    resp = client.table(TABLE_NAME).select("*").order("purchase_date", desc=True).execute()
    return [Purchase.model_validate(row) for row in resp.data]


def get_purchase_by_id(purchase_id: UUID) -> Purchase:
    """Retrieve a specific purchase by its ID.
    
    Args:
        purchase_id: Unique identifier of the purchase
        
    Returns:
        Purchase: The requested purchase record
        
    Raises:
        HTTPException: If purchase is not found or database operation fails
    """
    client: Client = get_supabase()
    resp = (
        client.table(TABLE_NAME)
        .select("*")
        .eq("id", str(purchase_id))
        .execute()
    )
    data = resp.data
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Purchase with id {purchase_id} not found"
        )
    return Purchase.model_validate(data[0])


def create_purchase(payload: PurchaseCreate) -> Purchase:
    """Create a new purchase in the database.
    
    Args:
        payload: Purchase creation data
        
    Returns:
        Purchase: The newly created purchase record
        
    Raises:
        HTTPException: If referenced category doesn't exist or creation fails
    """
    client: Client = get_supabase()
    
    # Validate category exists
    from app.db.repositories.category_repository import get_category_by_id
    get_category_by_id(payload.category_id)  # Will raise if not found
    
    data = serialize_for_supabase(payload.model_dump())
    resp = (
        client.table(TABLE_NAME)
        .insert(data)
        .execute()
    )
    return Purchase.model_validate(resp.data[0])


def update_purchase(purchase_id: UUID, payload: PurchaseUpdate) -> Purchase | None:
    """Update an existing purchase in the database.
    
    Args:
        purchase_id: Unique identifier of the purchase to update
        payload: Purchase update data (only non-None fields will be updated)
        
    Returns:
        Purchase | None: The updated purchase record, or None if no changes
        
    Raises:
        HTTPException: If purchase or referenced category is not found
    """
    client: Client = get_supabase()
    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if not update_data:
        return get_purchase_by_id(purchase_id)
    
    # Validate category exists if category_id is being updated
    if 'category_id' in update_data and update_data['category_id']:
        from app.db.repositories.category_repository import get_category_by_id
        get_category_by_id(update_data['category_id'])  # Will raise if not found
    
    update_data = serialize_for_supabase(update_data)

    resp = (
        client.table(TABLE_NAME)
        .update(update_data)
        .eq("id", str(purchase_id))
        .execute()
    )
    data = resp.data
    if not data:
        return None
    return Purchase.model_validate(data[0])


def delete_purchase(purchase_id: UUID) -> None:
    """Delete a purchase from the database.
    
    Args:
        purchase_id: Unique identifier of the purchase to delete
        
    Raises:
        HTTPException: If deletion fails
        
    Note:
        This operation will fail if there are transformations referencing this purchase
        due to foreign key constraints.
    """
    client: Client = get_supabase()
    client.table(TABLE_NAME).delete().eq("id", str(purchase_id)).execute()
