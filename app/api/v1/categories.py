"""Category API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, status, Query

from app.models.category import (
    Category,
    CategoryCreate,
    CategoryUpdate,
    CategoryPayload,
)
from app.api.deps import auth_service_depends, category_service_depends
from app.utils.auth import check_login
from app.services.auth_service import AuthService

router: APIRouter = APIRouter(prefix="/v1/categories", tags=["categories"])


@router.get("/", response_model=List[Category])
def get_categories(
    category_service: category_service_depends, payload: CategoryPayload = Query()
) -> List[Category]:
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
