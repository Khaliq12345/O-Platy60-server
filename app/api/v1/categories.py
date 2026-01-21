"""Category API endpoints.

This module defines REST API endpoints for category management,
including CRUD operations for food categories.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.db.repositories.category_repository import (
    list_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
)

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(prefix="/v1/categories", tags=["categories"])


@router.get("/", response_model=List[Category])
def get_categories() -> List[Category]:
    """Retrieve all categories.
    
    Returns:
        List[Category]: List of all available categories
        
    Raises:
        HTTPException: If database operation fails
    """
    return list_categories()


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category_endpoint(payload: CategoryCreate) -> Category:
    """Create a new category.
    
    Args:
        payload: Category creation data
        
    Returns:
        Category: The newly created category
        
    Raises:
        HTTPException: If creation fails or validation errors occur
    """
    return create_category(payload)


@router.put("/{category_id}", response_model=Category)
def update_category_endpoint(category_id: UUID, payload: CategoryUpdate) -> Category:
    """Update an existing category.
    
    Args:
        category_id: Unique identifier of the category to update
        payload: Category update data (only provided fields will be updated)
        
    Returns:
        Category: The updated category
        
    Raises:
        HTTPException: If category is not found or update fails
    """
    return update_category(category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_endpoint(category_id: UUID) -> None:
    """Delete a category.
    
    Args:
        category_id: Unique identifier of the category to delete
        
    Raises:
        HTTPException: If category is not found or deletion fails
        
    Note:
        This operation will fail if there are purchases referencing this category.
    """
    get_category_by_id(category_id)  # Validate exists
    delete_category(category_id)
