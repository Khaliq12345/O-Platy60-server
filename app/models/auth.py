from enum import Enum
from pydantic import BaseModel
from typing import Optional, Any
from app.models.users import User

class AuthForm(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    email: Optional[str] = None
    metadata: dict[str, Any]
    user: Optional[User] = None

class LogoutRequest(BaseModel):
    access_token: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class Role(Enum):
    ADMIN = "admin"
    MANAGER = "manager"

class SignupForm(AuthForm):
    full_name: str
    role: Role