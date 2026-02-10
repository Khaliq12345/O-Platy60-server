from typing import Dict, List

from fastapi import APIRouter, Query, status

from app.models.inventory import (
    InventoryCreate,
    InventoryResponse,
    InventoryUpdate,
    InventoryPayload,
)
from app.api.deps import inventory_service_depends

router = APIRouter(prefix="/v1/inventories", tags=["inventories"])


@router.get("/", response_model=Dict[str, List[InventoryResponse] | int])
def get_inventories(
    inventory_service: inventory_service_depends, payload: InventoryPayload = Query()
) -> Dict[str, List[InventoryResponse] | int]:
    """Retrieve all inventories"""
    return inventory_service.get_inventories(payload)


@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory(inventory_service: inventory_service_depends, inventory_id: str) -> InventoryResponse:
    """Retrieve a specific inventory by ID"""
    return inventory_service.get_inventory(inventory_id)


@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory(
    inventory_service: inventory_service_depends, payload: InventoryCreate
) -> InventoryResponse:
    """Create a new inventory"""
    return inventory_service.create_inventory(payload)


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_service: inventory_service_depends,
    inventory_id: str,
    payload: InventoryUpdate,
) -> InventoryResponse:
    """Update an existing inventory"""
    return inventory_service.update_inventory(inventory_id, payload)


@router.delete("/{inventory_id}")
def delete_inventory(
    inventory_service: inventory_service_depends, inventory_id: str
) -> None:
    """Delete an inventory"""
    inventory_service.delete_inventory(inventory_id)
