"""Configuration module for the O-Platy60 server application.

This module handles environment variable loading and exposes configuration
values needed throughout the application, particularly for Supabase integration.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase configuration
SUPABASE_URL: str | None = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY: str | None = os.getenv("SUPABASE_SERVICE_ROLE_KEY")