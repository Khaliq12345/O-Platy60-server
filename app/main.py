"""Main FastAPI application module.

This module creates and configures the FastAPI application instance,
including all API routes and middleware.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.exception import BusinessError 
from app.middleware.error_handler import business_exception_handler

# Create FastAPI application instance
app: FastAPI = FastAPI(
    title="O-Platy60 Server",
    description="API for managing food purchases and transformations",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include all API routes
app.include_router(api_router)

# Handler
app.add_exception_handler(BusinessError, business_exception_handler)

