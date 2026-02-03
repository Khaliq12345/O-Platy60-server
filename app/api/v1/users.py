"""User API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, status

from app.models.users import User, UserCreate, UserUpdate
from app.api.deps import user_service_depends

from app.utils.auth import check_login

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(
    prefix="/v1/users",
    tags=["users"],
    dependencies=[Depends(check_login)],
)


@router.get("/", response_model=List[User])
def get_users(user_service: user_service_depends) -> List[User]:
    """Retrieve all users."""
    return user_service.get_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_service: user_service_depends, user_id: str) -> User:
    """Retrieve a specific user by ID."""
    return user_service.get_user(user_id)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user_service: user_service_depends, payload: UserCreate
) -> User:
    """Create a new user."""
    return user_service.create_user(payload)


@router.put("/{user_id}", response_model=User)
def update_user_endpoint(
    user_service: user_service_depends, user_id: str, payload: UserUpdate
) -> User:
    """Update an existing user."""
    return user_service.update_user(user_id, payload)


@router.delete("/{user_id}")
def delete_user_endpoint(user_service: user_service_depends, user_id: str) -> None:
    """Delete a user."""
    user_service.delete_user(user_id)
