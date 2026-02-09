from typing import Dict, List
from app.models.inventory import InventoryCreate, InventoryUpdate, InventoryResponse, InventoryPayload
from app.db.repositories.inventory_repository import InventoryRepository
from app.core.exception import DatabaseError, ItemNotFoundError


class InventoryService:
    def __init__(self) -> None:
        self.repo = InventoryRepository()

    def get_inventories(self, payload: InventoryPayload) -> Dict[str, List[InventoryResponse] | int]:
        """Get all inventories with filters"""
        try:
            inventories, count = self.repo.list_inventories(
                search=payload.search,
                limit=payload.limit,
                offset=payload.offset,
                is_desc=payload.is_desc,
                start_date=payload.start_date if isinstance(payload.start_date, str) else None,
                end_date=payload.end_date if isinstance(payload.end_date, str) else None,
                category_id=payload.category_id,
            )
            return {"inventories": inventories, "count": count}
        except Exception as e:
            raise DatabaseError("get_inventories", str(e))

    def get_inventory(self, inventory_id: str) -> InventoryResponse:
        """Get a single inventory"""
        try:
            inventory = self.repo.get_by_id(inventory_id)
            if not inventory:
                raise ItemNotFoundError("get_inventory", inventory_id)
            return inventory
        except ItemNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError("get_inventory", str(e))

    def create_inventory(self, payload: InventoryCreate) -> InventoryResponse:
        """Create a new inventory"""
        try:
            inventory = self.repo.create(payload)
            return inventory
        except Exception as e:
            raise DatabaseError("create_inventory", str(e))

    def update_inventory(self, inventory_id: str, payload: InventoryUpdate) -> InventoryResponse:
        """Update an existing inventory"""
        try:
            inventory = self.repo.update(inventory_id, payload)
            if not inventory:
                raise ItemNotFoundError("update_inventory", inventory_id)
            return inventory
        except ItemNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError("update_inventory", str(e))

    def delete_inventory(self, inventory_id: str) -> None:
        """Delete an inventory"""
        try:
            self.get_inventory(inventory_id)
            self.repo.delete(inventory_id)
        except Exception as e:
            raise DatabaseError("delete_inventory", str(e))
