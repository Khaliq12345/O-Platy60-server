"""API router configuration.

This module aggregates all API version routers and creates the main
API router that will be included in the FastAPI application.
"""

from fastapi import APIRouter, Depends

from app.api.v1 import (
    auth,
    categories,
    inventory,
    products,
    purchases,
    transformations,
    ingredients,
    transformations_steps,
    users,
)
from app.utils.auth import check_login

# Create main API router
api_router: APIRouter = APIRouter()

# Include all v1 routers
api_router.include_router(auth.router)
api_router.include_router(categories.router, dependencies=[Depends(check_login)])
api_router.include_router(inventory.router, dependencies=[Depends(check_login)])
api_router.include_router(purchases.router, dependencies=[Depends(check_login)])
api_router.include_router(transformations.router, dependencies=[Depends(check_login)])
api_router.include_router(
    transformations_steps.router, dependencies=[Depends(check_login)]
)
api_router.include_router(ingredients.router, dependencies=[Depends(check_login)])
api_router.include_router(products.router, dependencies=[Depends(check_login)])
api_router.include_router(users.router)
