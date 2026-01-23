"""Transformation API endpoints."""

from typing import List
from fastapi import APIRouter, status

from app.models.transformation import (
    Transformation,
    TransformationCreate,
    TransformationUpdate,
)
from app.api.deps import transformation_service_depends

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(prefix="/v1/transformations", tags=["transformations"])


@router.get("/", response_model=List[Transformation])
def get_transformations(transformation_service: transformation_service_depends) -> List[Transformation]:
    """Retrieve all transformations."""
    return transformation_service.get_transformations()


@router.get("/{transformation_id}", response_model=Transformation)
def get_transformation(transformation_service: transformation_service_depends, transformation_id: str) -> Transformation:
    """Retrieve a specific transformation by ID."""
    return transformation_service.get_transformation(transformation_id)


@router.post("/", response_model=Transformation, status_code=status.HTTP_201_CREATED)
def create_transformation_endpoint(transformation_service: transformation_service_depends, payload: TransformationCreate) -> Transformation:
    """Create a new transformation."""
    return transformation_service.create_transformation(payload)


@router.put("/{transformation_id}", response_model=Transformation)
def update_transformation_endpoint(
    transformation_service: transformation_service_depends, transformation_id: str, payload: TransformationUpdate
) -> Transformation:
    """Update an existing transformation."""
    return transformation_service.update_transformation(transformation_id, payload)


@router.delete("/{transformation_id}")
def delete_transformation_endpoint(transformation_service: transformation_service_depends, transformation_id: str) -> None:
    """Delete a transformation."""
    transformation_service.delete_transformation(transformation_id)