"""Category API endpoints.

This module defines REST API endpoints for category management,
including CRUD operations for food categories.
"""

from typing import List
from fastapi import APIRouter, Query, status

from app.models.category import Category, CategoryCreate, CategoryUpdate, CategoryPayload
from app.api.deps import category_service_depends

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(prefix="/v1/categories", tags=["categories"])


@router.get("/", response_model=List[Category])
def get_categories(category_service: category_service_depends, payload: CategoryPayload = Query()) -> List[Category]:
    """Retrieve all categories.
    
    Returns:
        List[Category]: List of all available categories
    """
    return category_service.get_categories(payload)


@router.get("/{category_id}", response_model=Category)
def get_category(category_service: category_service_depends, category_id: str) -> Category:
    """Retrieve a specific category by ID.
    
    Args:
        category_id: Unique identifier of the category
        
    Returns:
        Category: The requested category record
    """
    return category_service.get_category(category_id)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category_endpoint(category_service: category_service_depends, payload: CategoryCreate) -> Category:
    """Create a new category.
    
    Args:
        payload: Category creation data
        
    Returns:
        Category: The newly created category
    """
    return category_service.create_category(payload)


@router.put("/{category_id}", response_model=Category)
def update_category_endpoint(category_service: category_service_depends, category_id: str, payload: CategoryUpdate) -> Category:
    """Update an existing category.
    
    Args:
        category_id: Unique identifier of the category to update
        payload: Category update data (only provided fields will be updated)
        
    Returns:
        Category: The updated category
    """
    return category_service.update_category(category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_endpoint(category_service: category_service_depends, category_id: str) -> None:
    """Delete a category.
    
    Args:
        category_id: Unique identifier of the category to delete
        
    Note:
        This operation will fail if there are purchases referencing this category.
    """
    category_service.delete_category(category_id)
