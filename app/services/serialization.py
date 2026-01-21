"""Data serialization utilities for Supabase integration.

This module provides functions to convert Python objects to JSON-serializable
formats required by Supabase API.
"""

from uuid import UUID
from datetime import date, datetime
from typing import Dict, Any


def serialize_for_supabase(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert UUID, date, and datetime objects to strings for JSON serialization.
    
    This function modifies the input dictionary in-place, converting any UUID,
    date, or datetime values to their ISO string representations.
    
    Args:
        data: Dictionary containing data to be serialized
        
    Returns:
        Dict[str, Any]: The same dictionary with serialized values
        
    Example:
        >>> data = {"id": UUID("123e4567-e89b-12d3-a456-426614174000"), "date": date.today()}
        >>> serialize_for_supabase(data)
        {"id": "123e4567-e89b-12d3-a456-426614174000", "date": "2024-01-01"}
    """
    for key, value in data.items():
        if isinstance(value, UUID):
            data[key] = str(value)
        elif isinstance(value, (date, datetime)):
            data[key] = value.isoformat()
    return data