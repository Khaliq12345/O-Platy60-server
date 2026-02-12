from typing import List, Tuple

from postgrest import CountMethod

from app.db.supabase import SUPABASE
from app.models.inventory import (
    InventoryCreate,
    InventoryResponse,
    InventoryTransaction,
    InventoryTransactionCreate,
    InventoryUpdate,
)

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
        self.client.table(TABLE_NAME).delete().eq(
            "inventory_id", inventory_id
        ).execute()

    def add_transaction(self, transaction: InventoryTransactionCreate):
        data = transaction.model_dump()
        older = self.get_day_transaction(
            transaction.created_at, transaction.inventory_id
        )
        if older:
            print("Existing transaction found")
            older.sale = transaction.sale
            self.client.table("inventory_transaction").update(older.model_dump()).eq(
                "id", older.id
            ).execute()
            return older
        print("No transaction found")
        response = self.client.table("inventory_transaction").insert(data).execute()
        return InventoryTransaction.model_validate(response.data[0])

    def get_transactions(
        self,
        inventory_id: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[InventoryTransaction]:

        query = (
            self.client.table("inventory_transaction")
            .select("*")
            .eq("inventory_id", inventory_id)
        )

        # Ajouter le filtre de date de début seulement si fourni
        if start_date is not None:
            query = query.gte("created_at", start_date)

        # Ajouter le filtre de date de fin seulement si fourni
        if end_date is not None:
            query = query.lte("created_at", end_date)

        response = query.execute()
        print(response.data)
        if len(response.data) > 0:
            return [InventoryTransaction.model_validate(item) for item in response.data]

        return []

    def get_day_transaction(
        self, date: str | None, inventory_id: str
    ) -> InventoryTransaction | None:
        if date is None:
            return None
        response = (
            self.client.table("inventory_transaction")
            .select("*")
            .eq("inventory_id", inventory_id)
            .gte("created_at", date)
            .lte("created_at", date)
            .execute()
        )
        if len(response.data) > 0:
            return InventoryTransaction.model_validate(response.data[0])
        return None
