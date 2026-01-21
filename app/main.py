"""Main FastAPI application module.

This module creates and configures the FastAPI application instance,
including all API routes and middleware.
"""

from fastapi import FastAPI
from app.api import api_router

# Create FastAPI application instance
app: FastAPI = FastAPI(
    title="O-Platy60 Server",
    description="API for managing food purchases and transformations",
    version="1.0.0"
)

# Include all API routes
app.include_router(api_router)