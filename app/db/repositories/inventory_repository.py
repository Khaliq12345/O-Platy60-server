from typing import List, Tuple

from postgrest import CountMethod
from app.db.supabase import SUPABASE
from app.models.inventory import InventoryCreate, InventoryUpdate, InventoryResponse

TABLE_NAME = "inventory"


class InventoryRepository(SUPABASE):
    def __init__(self):
        super().__init__()

    def list_inventories(
        self,
        search: str | None = None,
        category_id: str | None = None,
        limit: int = 20,
        offset: int = 0,
        is_desc: bool = True,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Tuple[List[InventoryResponse], int]:
        stmt = (
            self.client.table(TABLE_NAME)
            .select("*", count=CountMethod.exact)
            .limit(limit)
            .offset(offset)
            .order("created_at", desc=is_desc)
        )
        if search:
            stmt = stmt.ilike("name", f"%{search}%")
        if category_id:
            stmt = stmt.eq("category", category_id)
        if start_date:
            stmt = stmt.gte("created_at", start_date)
        if end_date:
            stmt = stmt.lte("created_at", end_date)

        resp = stmt.execute()
        return (
            [InventoryResponse.model_validate(row) for row in resp.data],
            resp.count if resp.count else 0,
        )

    def get_by_id(self, inventory_id: str) -> InventoryResponse | None:
        response = (
            self.client.table(TABLE_NAME)
            .select("*")
            .eq("inventory_id", inventory_id)
            .execute()
        )
        return (
            InventoryResponse.model_validate(response.data[0])
            if response.data
            else None
        )

    def create(self, inventory: InventoryCreate) -> InventoryResponse:
        data = inventory.model_dump()
        response = self.client.table(TABLE_NAME).insert(data).execute()
        return InventoryResponse.model_validate(response.data[0])

    def update(
        self, inventory_id: str, inventory: InventoryUpdate
    ) -> InventoryResponse | None:
        data = {k: v for k, v in inventory.model_dump(exclude_unset=True).items()}
        if not data:
            return self.get_by_id(inventory_id)

        response = (
            self.client.table(TABLE_NAME)
            .update(data)
            .eq("inventory_id", inventory_id)
            .execute()
        )
        return (
            InventoryResponse.model_validate(response.data[0])
            if response.data
            else None
        )

    def delete(self, inventory_id: str) -> None:
        self.client.table(TABLE_NAME).delete().eq("inventory_id", inventory_id).execute()
