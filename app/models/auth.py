from pydantic import BaseModel
from typing import Optional, Any

class AuthForm(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    email: Optional[str] = None
    metadata: dict[str, Any]

class LogoutRequest(BaseModel):
    access_token: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
