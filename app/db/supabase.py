"""Supabase database client configuration.

This module provides a factory function to create and configure
Supabase client instances for database operations.
"""

from supabase import Client, create_client
from app.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY


def get_supabase() -> Client:
    """Create and return a configured Supabase client.
    
    Returns:
        Client: Configured Supabase client instance
        
    Raises:
        ValueError: If required environment variables are not set
    """
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("Supabase configuration is missing")
        
    return create_client(
        SUPABASE_URL,
        SUPABASE_SERVICE_ROLE_KEY,
    )
