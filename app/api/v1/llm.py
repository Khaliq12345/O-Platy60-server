"""VOICE-TO-ACTION API endpoints.

This module defines REST API endpoints for VOICE-TO-ACTION management,
"""

from typing import Dict, List
from fastapi import APIRouter, Query

from app.models.purchase import Purchase, PurchasePayload
from app.api.deps import purchase_service_depends

# Create router with prefix and tags for OpenAPI documentation
router: APIRouter = APIRouter(prefix="/v1/llm", tags=["llm"])


@router.get("/audio", response_model=Dict[str, List[Purchase] | int])
def audio_to_object(
    purchase_service: purchase_service_depends, payload: PurchasePayload = Query()
) -> Dict[str, List[Purchase] | int]:
    """Retrieve all purchases."""
    return purchase_service.get_purchases(payload)
