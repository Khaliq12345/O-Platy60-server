"""API router configuration.

This module aggregates all API version routers and creates the main
API router that will be included in the FastAPI application.
"""

from fastapi import APIRouter
from .v1 import categories_router, purchases_router, transformations_router, transformations_steps_router

# Create main API router
api_router: APIRouter = APIRouter()

# Include all v1 routers
api_router.include_router(categories_router)
api_router.include_router(purchases_router)
api_router.include_router(transformations_router)
api_router.include_router(transformations_steps_router)