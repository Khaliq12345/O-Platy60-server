"""Transformation API endpoints."""

from typing import Dict, List
from fastapi import APIRouter, Depends, Query, status

from app.models.transformation import (
    Transformation,
    TransformationCreate,
    TransformationPayload,
    TransformationUpdate,
    TransformationSummary,
)
from app.api.deps import transformation_service_depends
from app.utils.auth import check_login

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(
    prefix="/v1/transformations",
    tags=["transformations"],
)


@router.get("/", response_model=Dict[str, List[Transformation] | int])
def get_transformations(
    transformation_service: transformation_service_depends,
    payload: TransformationPayload = Query(),
) -> List[Transformation]:
    """Retrieve all transformations."""
    return transformation_service.get_transformations(payload)


@router.get("/{transformation_id}", response_model=Transformation)
def get_transformation(
    transformation_service: transformation_service_depends, transformation_id: str
) -> Transformation:
    """Retrieve a specific transformation by ID."""
    return transformation_service.get_transformation(transformation_id)


@router.get("/purchase/{purchase_id}", response_model=Transformation)
def get_purchase_transformation(
    transformation_service: transformation_service_depends, purchase_id: str
) -> Transformation:
    """Retrieve a specific transformation by Purchase ID."""
    return transformation_service.get_transformation_by_purchase(purchase_id)


@router.get("/{transformation_id}/summary", response_model=TransformationSummary)
def get_transformation_summary(
    transformation_service: transformation_service_depends, transformation_id: str
) -> TransformationSummary:
    """Retrieve transformation summary with step calculations."""
    return transformation_service.transformation_summary(transformation_id)


@router.post("/", response_model=Transformation, status_code=status.HTTP_201_CREATED)
def create_transformation_endpoint(
    transformation_service: transformation_service_depends,
    payload: TransformationCreate,
) -> Transformation:
    """Create a new transformation."""
    return transformation_service.create_transformation(payload)


@router.put("/{transformation_id}", response_model=Transformation)
def update_transformation_endpoint(
    transformation_service: transformation_service_depends,
    transformation_id: str,
    payload: TransformationUpdate,
) -> Transformation:
    """Update an existing transformation."""
    return transformation_service.update_transformation(transformation_id, payload)


@router.delete("/{transformation_id}")
def delete_transformation_endpoint(
    transformation_service: transformation_service_depends, transformation_id: str
) -> None:
    """Delete a transformation."""
    transformation_service.delete_transformation(transformation_id)
