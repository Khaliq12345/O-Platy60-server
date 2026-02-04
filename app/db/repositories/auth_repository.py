"""Auth repository for authentication operations.

This module provides data access layer functions for authentication,
handling login and logout operations with Supabase auth.
"""

from typing import Dict, Any

from app.db.supabase import SUPABASE
from app.models.auth import AuthForm, AuthResponse


class AuthRepo(SUPABASE):
    def __init__(self) -> None:
        super().__init__()

    def sign_in(self, form: AuthForm) -> AuthResponse:
        """Authenticate user with email and password"""
        response = self.client.auth.sign_in_with_password(
            {"email": form.email, "password": form.password}
        )

        if not response.user or not response.session:
            raise Exception("Invalid credentials")

        return AuthResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=response.user.id,
            email=response.user.email,
            metadata=response.user.user_metadata,
        )

    def sign_out(self) -> Dict[str, str]:
        """Sign out user"""
        self.client.auth.sign_out()
        return {"message": "Successfully logged out"}

    def validate_token(self, token: str) -> bool:
        """Validate user token and check user status"""
        response = self.client.auth.get_user(token)
        
        if not response.user or not response.user.id:
            return False
            
        return True

    def refresh_session(self, refresh_token: str) -> AuthResponse:
        """Refresh user session with refresh token"""
        response = self.client.auth.refresh_session(refresh_token)
        
        return AuthResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=response.user.id,
            email=response.user.email,
            metadata=response.user.user_metadata,
        )
