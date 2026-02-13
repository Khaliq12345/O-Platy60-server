from typing import Dict, List

from app.core.exception import DatabaseError, ItemNotFoundError
from app.db.repositories.inventory_repository import InventoryRepository
from app.models.inventory import (
    InventoryCreate,
    InventoryPayload,
    InventoryResponse,
    InventoryTransaction,
    InventoryTransactionCreate,
    InventoryUpdate,
    InventoryWeeklySummary,
    InventoryWeeklySummaryQuery,
)


class InventoryService:
    def __init__(self) -> None:
        self.repo = InventoryRepository()

    def get_inventories(
        self, payload: InventoryPayload
    ) -> Dict[str, List[InventoryResponse] | int]:
        """Get all inventories with filters"""
        try:
            inventories, count = self.repo.list_inventories(
                search=payload.search,
                limit=payload.limit,
                offset=payload.offset,
                is_desc=payload.is_desc,
                start_date=payload.start_date
                if isinstance(payload.start_date, str)
                else None,
                end_date=payload.end_date
                if isinstance(payload.end_date, str)
                else None,
                category_id=payload.category_id,
            )
            return {"inventories": inventories, "count": count}
        except Exception as e:
            raise DatabaseError("get_inventories", str(e))

    def get_inventory(self, inventory_id: str) -> InventoryResponse:
        """Get a single inventory"""
        print("unsupposed call")
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

    def update_inventory(
        self, inventory_id: str, payload: InventoryUpdate
    ) -> InventoryResponse:
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

    def add_transaction(
        self, payload: InventoryTransactionCreate
    ) -> InventoryTransaction:
        """Add a transaction to an inventory"""
        try:
            transaction = self.repo.add_transaction(payload)
            return transaction
        except Exception as e:
            raise DatabaseError("add_transaction", str(e))

    def get_transactions(
        self, inventory_id: str, payload: InventoryPayload
    ) -> List[InventoryTransaction]:
        """Retrieve all transactions for a specific inventory"""
        try:
            transactions = self.repo.get_transactions(
                inventory_id=inventory_id,
                start_date=payload.start_date,
                end_date=payload.end_date,
            )
            return transactions
        except Exception as e:
            raise DatabaseError("get_transactions", str(e))

    def get_weekly_summary(
        self, payload: InventoryWeeklySummaryQuery
    ) -> InventoryWeeklySummary:
        """Retrieve weekly summary for a specific inventory"""
        try:
            summary = self.repo.get_weekly_summary(payload)
            return summary
        except Exception as e:
            raise DatabaseError("get_weekly_summary", str(e))
