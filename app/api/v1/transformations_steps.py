"""Transformation step API endpoints.

This module defines REST API endpoints for transformation step management,
including CRUD operations for individual steps within transformation processes.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.models.transformation_step import (
    TransformationStep,
    TransformationStepCreate,
    TransformationStepUpdate,
)
from app.db.repositories.transformation_step_repository import (
    list_steps_by_transformation,
    get_step_by_id,
    create_step,
    update_step,
    delete_step,
)

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(prefix="/v1/transformation-steps", tags=["transformation-steps"])


@router.get("/{transformation_id}/", response_model=List[TransformationStep])
def get_steps_for_transformation(transformation_id: UUID) -> List[TransformationStep]:
    """Retrieve all steps for a specific transformation.
    
    Args:
        transformation_id: Unique identifier of the parent transformation
        
    Returns:
        List[TransformationStep]: List of steps ordered by creation time
        
    Raises:
        HTTPException: If database operation fails
    """
    return list_steps_by_transformation(transformation_id)


@router.get("/step/{step_id}", response_model=TransformationStep)
def get_step(step_id: UUID) -> TransformationStep:
    """Retrieve a specific transformation step by ID.
    
    Args:
        step_id: Unique identifier of the transformation step
        
    Returns:
        TransformationStep: The requested transformation step record
        
    Raises:
        HTTPException: If step is not found
    """
    return get_step_by_id(step_id)


@router.post("/", response_model=TransformationStep, status_code=status.HTTP_201_CREATED)
def create_step_endpoint(payload: TransformationStepCreate) -> TransformationStep:
    """Create a new transformation step.
    
    Args:
        payload: Step creation data including transformation reference
        
    Returns:
        TransformationStep: The newly created transformation step
        
    Raises:
        HTTPException: If referenced transformation doesn't exist or creation fails
    """
    return create_step(payload)


@router.put("/{step_id}", response_model=TransformationStep)
def update_step_endpoint(step_id: UUID, payload: TransformationStepUpdate) -> TransformationStep:
    """Update an existing transformation step.
    
    Args:
        step_id: Unique identifier of the step to update
        payload: Step update data (only provided fields will be updated)
        
    Returns:
        TransformationStep: The updated transformation step
        
    Raises:
        HTTPException: If step or referenced transformation is not found
    """
    return update_step(step_id, payload)


@router.delete("/{step_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_step_endpoint(step_id: UUID) -> None:
    """Delete a transformation step.
    
    Args:
        step_id: Unique identifier of the step to delete
        
    Raises:
        HTTPException: If step is not found
    """
    get_step_by_id(step_id)  # Validate exists
    delete_step(step_id)
