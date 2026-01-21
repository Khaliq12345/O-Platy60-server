"""User repository for database operations.

This module provides data access layer functions for user entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List
from uuid import UUID
from supabase import Client
from fastapi import HTTPException, status
from app.db.supabase import get_supabase
from app.services.serialization import serialize_for_supabase
from app.models.users import User, UserCreate, UserUpdate


# Database table name for users
TABLE_NAME: str = "users"


def list_users() -> List[User]:
    """Retrieve all users from the database.
    
    Returns:
        List[User]: List of all user records
        
    Raises:
        HTTPException: If database operation fails
    """
    client: Client = get_supabase()
    resp = client.table(TABLE_NAME).select("*").execute()
    return [User.model_validate(row) for row in resp.data]


def get_user_by_id(user_id: UUID) -> User:
    """Retrieve a specific user by their ID.
    
    Args:
        user_id: Unique identifier of the user
        
    Returns:
        User: The requested user record
        
    Raises:
        HTTPException: If user is not found or database operation fails
    """
    client: Client = get_supabase()
    resp = (
        client.table(TABLE_NAME)
        .select("*")
        .eq("id", str(user_id))
        .execute()
    )
    data = resp.data
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id {user_id} not found"
        )
    return User.model_validate(data[0])


def create_user(payload: UserCreate) -> User:
    """Create a new user in the database.
    
    Args:
        payload: User creation data
        
    Returns:
        User: The newly created user record
        
    Raises:
        HTTPException: If creation fails or validation errors occur
        
    Note:
        Email addresses must be unique across all users.
    """
    client: Client = get_supabase()
    data = serialize_for_supabase(payload.model_dump())
    resp = (
        client.table(TABLE_NAME)
        .insert(data)
        .execute()
    )
    return User.model_validate(resp.data[0])


def update_user(user_id: UUID, payload: UserUpdate) -> User | None:
    """Update an existing user in the database.
    
    Args:
        user_id: Unique identifier of the user to update
        payload: User update data (only non-None fields will be updated)
        
    Returns:
        User | None: The updated user record, or None if no changes
        
    Raises:
        HTTPException: If user is not found or update fails
    """
    client: Client = get_supabase()
    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if not update_data:
        return get_user_by_id(user_id)
    
    update_data = serialize_for_supabase(update_data)

    resp = (
        client.table(TABLE_NAME)
        .update(update_data)
        .eq("id", str(user_id))
        .execute()
    )
    data = resp.data
    if not data:
        return None
    return User.model_validate(data[0])


def delete_user(user_id: UUID) -> None:
    """Delete a user from the database.
    
    Args:
        user_id: Unique identifier of the user to delete
        
    Raises:
        HTTPException: If deletion fails
        
    Note:
        This operation will fail if there are purchases created by this user
        due to foreign key constraints.
    """
    client: Client = get_supabase()
    client.table(TABLE_NAME).delete().eq("id", str(user_id)).execute()
