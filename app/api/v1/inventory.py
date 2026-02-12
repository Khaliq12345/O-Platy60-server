from typing import Dict, List

from fastapi import APIRouter, Query, status

from app.api.deps import inventory_service_depends
from app.models.inventory import (
    InventoryCreate,
    InventoryPayload,
    InventoryResponse,
    InventoryTransaction,
    InventoryTransactionCreate,
    InventoryUpdate,
)

router = APIRouter(prefix="/v1/inventories", tags=["inventories"])


@router.get("/", response_model=Dict[str, List[InventoryResponse] | int])
def get_inventories(
    inventory_service: inventory_service_depends, payload: InventoryPayload = Query()
) -> Dict[str, List[InventoryResponse] | int]:
    """Retrieve all inventories"""
    return inventory_service.get_inventories(payload)


@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory(
    inventory_service: inventory_service_depends, inventory_id: str
) -> InventoryResponse:
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


@router.post(
    "/transactions",
    response_model=InventoryTransaction,
    status_code=status.HTTP_201_CREATED,
)
def add_transaction(
    inventory_service: inventory_service_depends,
    payload: InventoryTransactionCreate,
) -> InventoryTransaction:
    """Add a transaction to an inventory"""
    return inventory_service.add_transaction(payload)


@router.get("/{inventory_id}/transactions", response_model=List[InventoryTransaction])
def get_transactions(
    inventory_service: inventory_service_depends,
    inventory_id: str,
    payload: InventoryPayload = Query(),
) -> List[InventoryTransaction]:
    """Retrieve all transactions for a specific inventory"""
    return inventory_service.get_transactions(inventory_id, payload)
