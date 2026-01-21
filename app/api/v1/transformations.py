"""Transformation API endpoints.

This module defines REST API endpoints for transformation management,
including CRUD operations for food transformation processes.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.models.transformation import (
    Transformation,
    TransformationCreate,
    TransformationUpdate,
)
from app.db.repositories.transformation_repository import (
    list_transformations,
    get_transformation_by_id,
    create_transformation,
    update_transformation,
    delete_transformation,
)

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(prefix="/v1/transformations", tags=["transformations"])


@router.get("/", response_model=List[Transformation])
def get_transformations() -> List[Transformation]:
    """Retrieve all transformations.
    
    Returns:
        List[Transformation]: List of all transformations ordered by date (newest first)
        
    Raises:
        HTTPException: If database operation fails
    """
    return list_transformations()


@router.get("/{transformation_id}", response_model=Transformation)
def get_transformation(transformation_id: UUID) -> Transformation:
    """Retrieve a specific transformation by ID.
    
    Args:
        transformation_id: Unique identifier of the transformation
        
    Returns:
        Transformation: The requested transformation record
        
    Raises:
        HTTPException: If transformation is not found
    """
    return get_transformation_by_id(transformation_id)


@router.post("/", response_model=Transformation, status_code=status.HTTP_201_CREATED)
def create_transformation_endpoint(payload: TransformationCreate) -> Transformation:
    """Create a new transformation.
    
    Args:
        payload: Transformation creation data including purchase reference
        
    Returns:
        Transformation: The newly created transformation
        
    Raises:
        HTTPException: If referenced purchase doesn't exist or creation fails
    """
    return create_transformation(payload)


@router.put("/{transformation_id}", response_model=Transformation)
def update_transformation_endpoint(
    transformation_id: UUID, payload: TransformationUpdate
) -> Transformation:
    """Update an existing transformation.
    
    Args:
        transformation_id: Unique identifier of the transformation to update
        payload: Transformation update data (only provided fields will be updated)
        
    Returns:
        Transformation: The updated transformation
        
    Raises:
        HTTPException: If transformation is not found or update fails
    """
    return update_transformation(transformation_id, payload)


@router.delete("/{transformation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transformation_endpoint(transformation_id: UUID) -> None:
    """Delete a transformation.
    
    Args:
        transformation_id: Unique identifier of the transformation to delete
        
    Raises:
        HTTPException: If transformation is not found
        
    Note:
        This will also delete all associated transformation steps due to cascade delete.
    """
    get_transformation_by_id(transformation_id)  # Validate exists
    delete_transformation(transformation_id)
