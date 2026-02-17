"""User data models."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    manager = "manager"
    cook = "cook"
    admin = "admin"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None


class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True