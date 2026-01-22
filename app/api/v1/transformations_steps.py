"""Transformation step API endpoints.

This module defines REST API endpoints for transformation step management,
including CRUD operations for individual steps within transformation processes.
"""

from typing import List
from fastapi import APIRouter, Query, status

from app.models.transformation_step import (
    TransformationStep,
    TransformationStepCreate,
    TransformationStepPayload,
    TransformationStepUpdate,
)
from app.api.deps import transformation_step_service_depends

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(prefix="/v1/transformation-steps", tags=["transformation-steps"])


@router.get("/{transformation_id}/", response_model=List[TransformationStep])
def get_steps_for_transformation(transformation_step_service: transformation_step_service_depends, transformation_id: str, payload: TransformationStepPayload = Query()) -> List[TransformationStep]:
    """Retrieve all steps for a specific transformation.
    
    Args:
        transformation_id: Unique identifier of the parent transformation
        
    Returns:
        List[TransformationStep]: List of steps ordered by creation time
    """
    return transformation_step_service.get_steps_by_transformation(transformation_id, payload)


@router.get("/step/{step_id}", response_model=TransformationStep)
def get_step(transformation_step_service: transformation_step_service_depends, step_id: str) -> TransformationStep:
    """Retrieve a specific transformation step by ID.
    
    Args:
        step_id: Unique identifier of the transformation step
        
    Returns:
        TransformationStep: The requested transformation step record
    """
    return transformation_step_service.get_step(step_id)


@router.post("/", response_model=TransformationStep, status_code=status.HTTP_201_CREATED)
def create_step_endpoint(transformation_step_service: transformation_step_service_depends, payload: TransformationStepCreate) -> TransformationStep:
    """Create a new transformation step.
    
    Args:
        payload: Step creation data including transformation reference
        
    Returns:
        TransformationStep: The newly created transformation step
    """
    return transformation_step_service.create_step(payload)


@router.put("/{step_id}", response_model=TransformationStep)
def update_step_endpoint(transformation_step_service: transformation_step_service_depends, step_id: str, payload: TransformationStepUpdate) -> TransformationStep:
    """Update an existing transformation step.
    
    Args:
        step_id: Unique identifier of the step to update
        payload: Step update data (only provided fields will be updated)
        
    Returns:
        TransformationStep: The updated transformation step
    """
    return transformation_step_service.update_step(step_id, payload)


@router.delete("/{step_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_step_endpoint(transformation_step_service: transformation_step_service_depends, step_id: str) -> None:
    """Delete a transformation step.
    
    Args:
        step_id: Unique identifier of the step to delete
    """
    transformation_step_service.delete_step(step_id)
