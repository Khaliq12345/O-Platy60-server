from typing import Dict, Any
from app.models.auth import AuthForm, AuthResponse, SignupForm
from app.db.repositories.auth_repository import AuthRepo
from app.core.exception import DatabaseError


class AuthService:
    def __init__(self) -> None:
        self.repo = AuthRepo()

    def login(self, form: AuthForm) -> AuthResponse:
        """Authenticate user with email and password"""
        try:
            return self.repo.sign_in(form)
        except Exception as e:
            raise DatabaseError("login", str(e))

    def logout(self, access_token: str) -> Dict[str, str]:
        """Sign out user"""
        try:
            return self.repo.sign_out()
        except Exception as e:
            raise DatabaseError("logout", str(e))

    def signup(self, form: SignupForm) -> AuthResponse:
        """Register new user with email and password"""
        try:
            return self.repo.sign_up(form)
        except Exception as e:
            raise DatabaseError("signup", str(e))

    def validate_token(self, token: str) -> bool:
        """Validate user token"""
        return self.repo.validate_token(token)

    def refresh_session(self, refresh_token: str) -> AuthResponse:
        """Refresh user session"""
        try:
            return self.repo.refresh_session(refresh_token)
        except Exception as e:
            raise DatabaseError("refresh_session", str(e))