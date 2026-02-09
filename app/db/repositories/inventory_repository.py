from typing import List, Optional

from app.db.supabase import SUPABASE
from app.models.inventory import InventoryCreate, InventoryUpdate, InventoryResponse

TABLE_NAME = "inventory"


class InventoryRepository(SUPABASE):
    def __init__(self):
        super().__init__()

    async def get_all(self) -> List[InventoryResponse]:
        response = self.client.table(TABLE_NAME).select("*").execute()
        return [InventoryResponse.model_validate(row) for row in response.data]

    async def get_by_id(self, inventory_id: str) -> InventoryResponse | None:
        response = (
            self.client.table(TABLE_NAME)
            .select("*")
            .eq("inventory_id", str(inventory_id))
            .execute()
        )

        return (
            InventoryResponse.model_validate(response.data[0])
            if response.data
            else None
        )

    async def create(self, inventory: InventoryCreate) -> InventoryResponse | None:
        data = inventory.model_dump()
        response = self.client.table(TABLE_NAME).insert(data).execute()
        return (
            InventoryResponse.model_validate(response.data[0])
            if response.data
            else None
        )

    async def update(
        self, inventory_id: str, inventory: InventoryUpdate
    ) -> InventoryResponse | None:
        data = {k: v for k, v in inventory.model_dump().items() if v is not None}
        if not data:
            return None

        response = (
            self.client.table(TABLE_NAME)
            .update(data)
            .eq("inventory_id", str(inventory_id))
            .execute()
        )
        return (
            InventoryResponse.model_validate(response.data[0])
            if response.data
            else None
        )

    async def delete(self, inventory_id: str) -> bool:
        response = (
            self.client.table(TABLE_NAME)
            .delete()
            .eq("inventory_id", str(inventory_id))
            .execute()
        )
        return len(response.data) > 0
