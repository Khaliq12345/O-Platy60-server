from typing import List, Optional

from app.db.supabase import SUPABASE
from app.models.inventory import InventoryCreate, InventoryUpdate

TABLE_NAME = "inventory"


class InventoryRepository(SUPABASE):
    def __init__(self):
        super().__init__()

    async def get_all(self) -> List[dict]:
        response = self.client.table(TABLE_NAME).select("*").execute()
        return response.data

    async def get_by_id(self, inventory_id: str) -> Optional[dict]:
        response = (
            self.client.table(TABLE_NAME)
            .select("*")
            .eq("inventory_id", str(inventory_id))
            .single()
            .execute()
        )
        return response.data if response.data else None

    async def create(self, inventory: InventoryCreate) -> dict:
        data = inventory.model_dump()
        response = self.client.table(TABLE_NAME).insert(data).execute()
        return response.data[0]

    async def update(
        self, inventory_id: str, inventory: InventoryUpdate
    ) -> Optional[dict]:
        data = {k: v for k, v in inventory.model_dump().items() if v is not None}
        if not data:
            return None

        response = (
            self.client.table(TABLE_NAME)
            .update(data)
            .eq("inventory_id", str(inventory_id))
            .execute()
        )
        return response.data[0] if response.data else None

    async def delete(self, inventory_id: str) -> bool:
        response = (
            self.client.table(TABLE_NAME)
            .delete()
            .eq("inventory_id", str(inventory_id))
            .execute()
        )
        return len(response.data) > 0
