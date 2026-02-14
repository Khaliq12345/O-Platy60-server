"""Category API endpoints."""

from typing import Dict, List

from fastapi import APIRouter, Query, status

from app.api.deps import category_service_depends
from app.models.category import (
    Category,
    CategoryCreate,
    CategoryPayload,
    CategoryUpdate,
)

router: APIRouter = APIRouter(prefix="/v1/categories", tags=["categories"])


@router.get("/", response_model=Dict[str, List[Category] | int])
def get_categories(
    category_service: category_service_depends, payload: CategoryPayload = Query()
) -> Dict[str, List[Category] | int]:
    """Retrieve all categories."""
    return category_service.get_categories(payload)


@router.get("/{category_id}", response_model=Category)
def get_category(
    category_service: category_service_depends, category_id: str
) -> Category:
    """Retrieve a specific category by ID."""
    return category_service.get_category(category_id)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category_endpoint(
    category_service: category_service_depends, payload: CategoryCreate
) -> Category:
    """Create a new category."""
    return category_service.create_category(payload)


@router.put("/{category_id}", response_model=Category)
def update_category_endpoint(
    category_service: category_service_depends,
    category_id: str,
    payload: CategoryUpdate,
) -> Category:
    """Update an existing category."""
    return category_service.update_category(category_id, payload)


@router.delete("/{category_id}")
def delete_category_endpoint(
    category_service: category_service_depends, category_id: str
) -> None:
    """Delete a category."""
    category_service.delete_category(category_id)
