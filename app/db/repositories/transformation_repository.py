"""Transformation repository for database operations.

This module provides data access layer functions for transformation entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List
from uuid import UUID
from supabase import Client
from fastapi import HTTPException, status
from app.services.serialization import serialize_for_supabase
from app.models.transformation import (
    Transformation,
    TransformationCreate,
    TransformationUpdate,
)


# Database table name for transformations
TABLE_NAME: str = "transformations"


def list_transformations() -> List[Transformation]:
    """Retrieve all transformations from the database.

    Returns:
        List[Transformation]: List of all transformation records ordered by date (newest first)

    Raises:
        HTTPException: If database operation fails
    """
    client: Client = get_supabase()
    resp = (
        client.table(TABLE_NAME)
        .select("*")
        .order("transformed_at", desc=True)
        .execute()
    )
    return [Transformation.model_validate(row) for row in resp.data]


def get_transformation_by_id(transformation_id: UUID) -> Transformation:
    """Retrieve a specific transformation by its ID.

    Args:
        transformation_id: Unique identifier of the transformation

    Returns:
        Transformation: The requested transformation record

    Raises:
        HTTPException: If transformation is not found or database operation fails
    """
    client: Client = get_supabase()
    resp = (
        client.table(TABLE_NAME).select("*").eq("id", str(transformation_id)).execute()
    )
    data = resp.data
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transformation with id {transformation_id} not found",
        )
    return Transformation.model_validate(data[0])


def create_transformation(payload: TransformationCreate) -> Transformation:
    """Create a new transformation in the database.

    Args:
        payload: Transformation creation data

    Returns:
        Transformation: The newly created transformation record

    Raises:
        HTTPException: If creation fails or validation errors occur

    Note:
        The purchase_id should reference an existing purchase record.
    """
    client: Client = get_supabase()
    data = serialize_for_supabase(payload.model_dump())
    resp = client.table(TABLE_NAME).insert(data).execute()
    return Transformation.model_validate(resp.data[0])


def update_transformation(
    transformation_id: UUID, payload: TransformationUpdate
) -> Transformation | None:
    """Update an existing transformation in the database.

    Args:
        transformation_id: Unique identifier of the transformation to update
        payload: Transformation update data (only non-None fields will be updated)

    Returns:
        Transformation | None: The updated transformation record, or None if no changes

    Raises:
        HTTPException: If transformation is not found or update fails
    """
    client: Client = get_supabase()
    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if not update_data:
        return get_transformation_by_id(transformation_id)

    update_data = serialize_for_supabase(update_data)

    resp = (
        client.table(TABLE_NAME)
        .update(update_data)
        .eq("id", str(transformation_id))
        .execute()
    )
    data = resp.data
    if not data:
        return None
    return Transformation.model_validate(data[0])


def delete_transformation(transformation_id: UUID) -> None:
    """Delete a transformation from the database.

    Args:
        transformation_id: Unique identifier of the transformation to delete

    Raises:
        HTTPException: If deletion fails

    Note:
        This operation will also delete all associated transformation steps
        due to cascade delete constraints.
    """
    client: Client = get_supabase()
    client.table(TABLE_NAME).delete().eq("id", str(transformation_id)).execute()
