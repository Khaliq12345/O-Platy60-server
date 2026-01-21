# app/db/repositories/category_repository.py
"""Category repository for database operations.

This module provides data access layer functions for category entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List
from uuid import UUID
from supabase import Client
from fastapi import HTTPException, status
from app.db.supabase import get_supabase
from app.services.serialization import serialize_for_supabase
from app.models.category import Category, CategoryCreate, CategoryUpdate


# Database table name for categories
TABLE_NAME: str = "categories"


def list_categories() -> List[Category]:
    """Retrieve all categories from the database.
    
    Returns:
        List[Category]: List of all category records
        
    Raises:
        HTTPException: If database operation fails
    """
    client: Client = get_supabase()
    resp = client.table(TABLE_NAME).select("*").execute()
    return [Category.model_validate(row) for row in resp.data]


def get_category_by_id(category_id: UUID) -> Category:
    """Retrieve a specific category by its ID.
    
    Args:
        category_id: Unique identifier of the category
        
    Returns:
        Category: The requested category record
        
    Raises:
        HTTPException: If category is not found or database operation fails
    """
    client: Client = get_supabase()
    resp = (
        client.table(TABLE_NAME)
        .select("*")
        .eq("id", str(category_id))
        .execute()
    )
    data = resp.data
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with id {category_id} not found"
        )
    return Category.model_validate(data[0])


def create_category(payload: CategoryCreate) -> Category:
    """Create a new category in the database.
    
    Args:
        payload: Category creation data
        
    Returns:
        Category: The newly created category record
        
    Raises:
        HTTPException: If creation fails or validation errors occur
    """
    client: Client = get_supabase()
    data = serialize_for_supabase(payload.model_dump())
    resp = (
        client.table(TABLE_NAME)
        .insert(data)
        .execute()
    )
    return Category.model_validate(resp.data[0])


def update_category(category_id: UUID, payload: CategoryUpdate) -> Category | None:
    """Update an existing category in the database.
    
    Args:
        category_id: Unique identifier of the category to update
        payload: Category update data (only non-None fields will be updated)
        
    Returns:
        Category | None: The updated category record, or None if no changes
        
    Raises:
        HTTPException: If category is not found or update fails
    """
    client: Client = get_supabase()
    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if not update_data:
        return get_category_by_id(category_id)
    
    update_data = serialize_for_supabase(update_data)

    resp = (
        client.table(TABLE_NAME)
        .update(update_data)
        .eq("id", str(category_id))
        .execute()
    )
    data = resp.data
    if not data:
        return None
    return Category.model_validate(data[0])


def delete_category(category_id: UUID) -> None:
    """Delete a category from the database.
    
    Args:
        category_id: Unique identifier of the category to delete
        
    Raises:
        HTTPException: If deletion fails
        
    Note:
        This operation will fail if there are purchases referencing this category
        due to foreign key constraints.
    """
    client: Client = get_supabase()
    client.table(TABLE_NAME).delete().eq("id", str(category_id)).execute()
