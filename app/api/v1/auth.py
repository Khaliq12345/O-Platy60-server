"""Auth API endpoints."""

from typing import Dict
from fastapi import APIRouter, HTTPException, status

from app.models.auth import AuthForm, AuthResponse, LogoutRequest, RefreshTokenRequest, ChangePasswordForm, SignupForm
from app.api.deps import auth_service_depends
from app.core.exception import DatabaseError

router: APIRouter = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/signup", response_model=AuthResponse)
def signup(form: SignupForm, auth_service: auth_service_depends):
    """Register new user with email and password"""
    try:
        return auth_service.signup(form)
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=AuthResponse)
def login(form: AuthForm, auth_service: auth_service_depends):
    """Authenticate user with email and passworwd"""
    try:
        return auth_service.login(form)
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/logout", response_model=Dict[str, str])
def logout(request: LogoutRequest, auth_service: auth_service_depends):
    """Sign out user"""
    try:
        return auth_service.logout(request.access_token)
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/refresh", response_model=AuthResponse)
def refresh(request: RefreshTokenRequest, auth_service: auth_service_depends):
    """Refresh user session"""
    try:
        return auth_service.refresh_session(request.refresh_token)
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/change-password")
def change_password(request: ChangePasswordForm, auth_service: auth_service_depends):
    """Change user password"""
    try:
        return auth_service.change_password(request)
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )