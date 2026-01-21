"""User data models.

This module defines Pydantic models for user entities, including
user roles, authentication, and profile information.
"""

from datetime import datetime
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """Enumeration of available user roles.
    
    Attributes:
        manager: Can manage purchases and view reports
        cook: Can create transformations and transformation steps
        admin: Full system access
    """
    manager = "manager"
    cook = "cook"
    admin = "admin"


class UserBase(BaseModel):
    """Base user model with common fields.
    
    Attributes:
        email: User's email address (used for authentication)
        full_name: User's full display name
        role: User's role in the system
    """
    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(..., description="User's full display name", min_length=1, max_length=200)
    role: UserRole = Field(..., description="User's role in the system")


class UserCreate(UserBase):
    """Schema for creating a new user.
    
    Inherits all fields from UserBase.
    """
    pass


class UserUpdate(BaseModel):
    """Schema for updating an existing user.
    
    All fields are optional to allow partial updates.
    """
    email: EmailStr | None = Field(None, description="Updated email address")
    full_name: str | None = Field(None, description="Updated full name", min_length=1, max_length=200)
    role: UserRole | None = Field(None, description="Updated user role")


class User(UserBase):
    """Complete user model with database fields.
    
    Includes all base fields plus database-generated fields.
    
    Attributes:
        id: Unique user identifier
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    id: UUID = Field(..., description="Unique user identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
