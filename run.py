"""Application entry point for development server.

This module provides a convenient way to start the FastAPI application
using Uvicorn ASGI server with development settings.

Usage:
    python run.py
"""

import uvicorn

if __name__ == "__main__":
    # Start the FastAPI application with Uvicorn
    uvicorn.run(
        "app.main:app",  # Application module and instance
        host="0.0.0.0",   # Listen on all interfaces
        port=8000,        # Default port
        reload=True       # Auto-reload on code changes (development only)
    )