"""Auth repository for authentication operations.

This module provides data access layer functions for authentication,
handling login and logout operations with Supabase auth.
"""

from typing import Dict, Any

from app.db.supabase import SUPABASE
from app.models.auth import AuthForm, AuthResponse, SignupForm
from app.models.users import UserCreate, User
from app.db.repositories.users_repository import UserRepo


class AuthRepo(SUPABASE):
    def __init__(self) -> None:
        super().__init__()
        self.user_repo = UserRepo()

    def sign_in(self, form: AuthForm) -> AuthResponse:
        """Authenticate user with email and password"""
        response = self.client.auth.sign_in_with_password(
            {"email": form.email, "password": form.password}
        )

        if not response.user or not response.session:
            raise Exception("Invalid credentials")

        # Get user data from users table
        user_data = self.client.table("users").select("*").eq("email", form.email).execute()
        
        if user_data.data and len(user_data.data) > 0:
            user = User.model_validate(user_data.data[0])
        else:
            # Create user record from auth metadata if not found
            metadata = response.user.user_metadata or {}
            user_create = UserCreate(
                email=form.email,
                full_name=metadata.get("full_name", ""),
                role=metadata.get("role", "manager")
            )
            user = self.user_repo.create_user(user_create)

        return AuthResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=response.user.id,
            email=response.user.email,
            metadata=response.user.user_metadata,
            user=user
        )

    def sign_up(self, form: SignupForm) -> AuthResponse:
        """Register new user with email and password"""
        response = self.client.auth.sign_up({
            "email": form.email,
            "password": form.password,
            "options": {
                "data": {
                    "full_name": form.full_name,
                    "role": form.role.value
                }
            }
        })

        if not response.user:
            raise Exception("Signup failed")

        # Create user record in users table
        user_create = UserCreate(
            email=form.email,
            full_name=form.full_name,
            role=form.role.value
        )
        user = self.user_repo.create_user(user_create)

        return AuthResponse(
            access_token="",
            refresh_token="",
            user_id=response.user.id,
            email=response.user.email,
            metadata=response.user.user_metadata,
            user=user
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
