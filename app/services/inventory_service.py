from typing import List
from app.models.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.db.repositories.inventory_repository import InventoryRepository
from app.core.exception import DatabaseError, ItemNotFoundError


class InventoryService:
    def __init__(self) -> None:
        self.repo = InventoryRepository()

    async def get_all_inventories(self) -> List[InventoryResponse]:
        """Get all inventories"""
        try:
            inventories = await self.repo.get_all()
            return inventories
        except Exception as e:
            raise DatabaseError("get_all_inventories", str(e))

    async def get_inventory(self, inventory_id: str) -> InventoryResponse:
        """Get a single inventory"""
        try:
            inventory = await self.repo.get_by_id(inventory_id)
            if not inventory:
                raise ItemNotFoundError("get_inventory", str(inventory_id))
            return inventory
        except ItemNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError("get_inventory", str(e))

    async def create_inventory(self, payload: InventoryCreate) -> InventoryResponse | None:
        """Create a new inventory"""
        try:
            inventory = await self.repo.create(payload)
            return inventory
        except Exception as e:
            raise DatabaseError("create_inventory", str(e))

    async def update_inventory(
        self, inventory_id: str, payload: InventoryUpdate
    ) -> InventoryResponse:
        """Update an existing inventory"""
        try:
            inventory = await self.repo.update(inventory_id, payload)
            if not inventory:
                raise ItemNotFoundError("update_inventory", str(inventory_id))
            return inventory
        except ItemNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError("update_inventory", str(e))

    async def delete_inventory(self, inventory_id: str) -> None:
        """Delete an inventory"""
        try:
            await self.get_inventory(inventory_id)
            await self.repo.delete(inventory_id)
        except Exception as e:
            raise DatabaseError("delete_inventory", str(e))
