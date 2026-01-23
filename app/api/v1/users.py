"""User API endpoints.

This module defines REST API endpoints for user management,
including CRUD operations for system users.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, status

from app.models.users import User, UserCreate, UserUpdate
from app.api.deps import user_service_depends

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(prefix="/v1/users", tags=["users"])


@router.get("/", response_model=List[User])
def get_users(user_service: user_service_depends) -> List[User]:
    """Retrieve all users.
    
    Returns:
        List[User]: List of all system users
    """
    return user_service.get_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_service: user_service_depends, user_id: UUID) -> User:
    """Retrieve a specific user by ID.
    
    Args:
        user_id: Unique identifier of the user
        
    Returns:
        User: The requested user record
    """
    return user_service.get_user(user_id)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_service: user_service_depends, payload: UserCreate) -> User:
    """Create a new user.
    
    Args:
        payload: User creation data
        
    Returns:
        User: The newly created user
        
    Note:
        Email addresses must be unique across all users.
    """
    return user_service.create_user(payload)


@router.put("/{user_id}", response_model=User)
def update_user_endpoint(user_service: user_service_depends, user_id: UUID, payload: UserUpdate) -> User:
    """Update an existing user.
    
    Args:
        user_id: Unique identifier of the user to update
        payload: User update data (only provided fields will be updated)
        
    Returns:
        User: The updated user
    """
    return user_service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_service: user_service_depends, user_id: UUID) -> None:
    """Delete a user.
    
    Args:
        user_id: Unique identifier of the user to delete
        
    Note:
        This operation will fail if there are purchases created by this user
        due to foreign key constraints.
    """
    user_service.delete_user(user_id)