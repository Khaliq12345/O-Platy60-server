"""API router configuration.

This module aggregates all API version routers and creates the main
API router that will be included in the FastAPI application.
"""

from fastapi import APIRouter
from app.api.v1 import (
    categories,
    purchases,
    transformations,
    transformations_steps,
)

# Create main API router
api_router: APIRouter = APIRouter()

# Include all v1 routers
api_router.include_router(categories.router)
api_router.include_router(purchases.router)
api_router.include_router(transformations.router)
api_router.include_router(transformations_steps.router)

