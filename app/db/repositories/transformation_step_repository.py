"""Transformation step repository for database operations.

This module provides data access layer functions for transformation step entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List
from uuid import UUID
from supabase import Client
from fastapi import HTTPException, status
from app.db.supabase import get_supabase
from app.services.serialization import serialize_for_supabase
from app.models.transformation_step import (
    TransformationStep,
    TransformationStepCreate,
    TransformationStepUpdate,
)


# Database table name for transformation steps
TABLE_NAME: str = "transformation_steps"


def list_steps_by_transformation(transformation_id: UUID) -> List[TransformationStep]:
    """Retrieve all transformation steps for a specific transformation.
    
    Args:
        transformation_id: Unique identifier of the parent transformation
        
    Returns:
        List[TransformationStep]: List of transformation steps ordered by creation time
        
    Raises:
        HTTPException: If database operation fails
    """
    client: Client = get_supabase()
    resp = (
        client.table(TABLE_NAME)
        .select("*")
        .eq("transformation_id", str(transformation_id))
        .order("created_at", asc=True)
        .execute()
    )
    return [TransformationStep.model_validate(row) for row in resp.data]


def get_step_by_id(step_id: UUID) -> TransformationStep:
    """Retrieve a specific transformation step by its ID.
    
    Args:
        step_id: Unique identifier of the transformation step
        
    Returns:
        TransformationStep: The requested transformation step record
        
    Raises:
        HTTPException: If step is not found or database operation fails
    """
    client: Client = get_supabase()
    resp = (
        client.table(TABLE_NAME)
        .select("*")
        .eq("id", str(step_id))
        .execute()
    )
    data = resp.data
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Transformation step with id {step_id} not found"
        )
    return TransformationStep.model_validate(data[0])


def create_step(payload: TransformationStepCreate) -> TransformationStep:
    """Create a new transformation step in the database.
    
    Args:
        payload: Transformation step creation data
        
    Returns:
        TransformationStep: The newly created transformation step record
        
    Raises:
        HTTPException: If parent transformation doesn't exist or creation fails
    """
    client: Client = get_supabase()
    
    # Validate transformation exists
    from app.db.repositories.transformation_repository import get_transformation_by_id
    get_transformation_by_id(payload.transformation_id)  # Will raise if not found
    
    data = serialize_for_supabase(payload.model_dump())
    resp = (
        client.table(TABLE_NAME)
        .insert(data)
        .execute()
    )
    return TransformationStep.model_validate(resp.data[0])


def update_step(step_id: UUID, payload: TransformationStepUpdate) -> TransformationStep | None:
    """Update an existing transformation step in the database.
    
    Args:
        step_id: Unique identifier of the step to update
        payload: Step update data (only non-None fields will be updated)
        
    Returns:
        TransformationStep | None: The updated step record, or None if no changes
        
    Raises:
        HTTPException: If step or referenced transformation is not found
    """
    client: Client = get_supabase()
    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if not update_data:
        return get_step_by_id(step_id)
    
    # Validate transformation exists if transformation_id is being updated
    if 'transformation_id' in update_data and update_data['transformation_id']:
        from app.db.repositories.transformation_repository import get_transformation_by_id
        get_transformation_by_id(update_data['transformation_id'])  # Will raise if not found
    
    update_data = serialize_for_supabase(update_data)

    resp = (
        client.table(TABLE_NAME)
        .update(update_data)
        .eq("id", str(step_id))
        .execute()
    )
    data = resp.data
    if not data:
        return None
    return TransformationStep.model_validate(data[0])


def delete_step(step_id: UUID) -> None:
    """Delete a transformation step from the database.
    
    Args:
        step_id: Unique identifier of the step to delete
        
    Raises:
        HTTPException: If deletion fails
    """
    client: Client = get_supabase()
    client.table(TABLE_NAME).delete().eq("id", str(step_id)).execute()
