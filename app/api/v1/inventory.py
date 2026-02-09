from typing import List

from fastapi import APIRouter, status

from app.models.inventory import InventoryCreate, InventoryResponse, InventoryUpdate
from app.api.deps import inventory_service_depends

router = APIRouter(prefix="/v1/inventories", tags=["inventories"])


@router.get("/", response_model=List[InventoryResponse])
async def get_inventories(inventory_service: inventory_service_depends):
    """Retrieve all inventories"""
    return await inventory_service.get_all_inventories()


@router.get("/{inventory_id}", response_model=InventoryResponse)
async def get_inventory(inventory_service: inventory_service_depends, inventory_id: str):
    """Retrieve a specific inventory by ID"""
    return await inventory_service.get_inventory(inventory_id)


@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    inventory_service: inventory_service_depends, payload: InventoryCreate
):
    """Create a new inventory"""
    return await inventory_service.create_inventory(payload)


@router.put("/{inventory_id}", response_model=InventoryResponse)
async def update_inventory(
    inventory_service: inventory_service_depends,
    inventory_id: str,
    payload: InventoryUpdate,
):
    """Update an existing inventory"""
    return await inventory_service.update_inventory(inventory_id, payload)


@router.delete("/{inventory_id}")
async def delete_inventory(
    inventory_service: inventory_service_depends, inventory_id: str
):
    """Delete an inventory"""
    await inventory_service.delete_inventory(inventory_id)
