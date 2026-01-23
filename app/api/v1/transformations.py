"""Transformation API endpoints.

This module defines REST API endpoints for transformation management,
including CRUD operations for food transformation processes.
"""

from typing import List
from uuid import UUID
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
    """Retrieve all transformations.
    
    Returns:
        List[Transformation]: List of all transformations ordered by date (newest first)
    """
    return transformation_service.get_transformations()


@router.get("/{transformation_id}", response_model=Transformation)
def get_transformation(transformation_service: transformation_service_depends, transformation_id: UUID) -> Transformation:
    """Retrieve a specific transformation by ID.
    
    Args:
        transformation_id: Unique identifier of the transformation
        
    Returns:
        Transformation: The requested transformation record
    """
    return transformation_service.get_transformation(transformation_id)


@router.post("/", response_model=Transformation, status_code=status.HTTP_201_CREATED)
def create_transformation_endpoint(transformation_service: transformation_service_depends, payload: TransformationCreate) -> Transformation:
    """Create a new transformation.
    
    Args:
        payload: Transformation creation data including purchase reference
        
    Returns:
        Transformation: The newly created transformation
    """
    return transformation_service.create_transformation(payload)


@router.put("/{transformation_id}", response_model=Transformation)
def update_transformation_endpoint(
    transformation_service: transformation_service_depends, transformation_id: UUID, payload: TransformationUpdate
) -> Transformation:
    """Update an existing transformation.
    
    Args:
        transformation_id: Unique identifier of the transformation to update
        payload: Transformation update data (only provided fields will be updated)
        
    Returns:
        Transformation: The updated transformation
    """
    return transformation_service.update_transformation(transformation_id, payload)


@router.delete("/{transformation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transformation_endpoint(transformation_service: transformation_service_depends, transformation_id: UUID) -> None:
    """Delete a transformation.
    
    Args:
        transformation_id: Unique identifier of the transformation to delete
        
    Note:
        This will also delete all associated transformation steps due to cascade delete.
    """
    transformation_service.delete_transformation(transformation_id)
