"""Purchase repository for database operations.

This module provides data access layer functions for purchase entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List, Tuple

from postgrest import CountMethod

from app.db.supabase import SUPABASE
from app.models.purchase import (
    Purchase,
    PurchaseCreate,
)
from app.services.serialization import serialize_for_supabase

# Database table name for purchases
TABLE_NAME: str = "purchases"


class PurchaseRepo(SUPABASE):
    def __init__(self) -> None:
        super().__init__()

    def list_purchases(
        self,
        search: str | None = None,
        category_id: str | None = None,
        created_by: str | None = None,
        limit: int = 20,
        offset: int = 0,
        is_desc: bool = True,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Tuple[List[Purchase], int]:
        """Retrieve all purchases from the database.

        Returns:
            List[Purchase]: List of all purchase records ordered by date (newest first)
        """
        stmt = (
            self.client.table(TABLE_NAME)
            .select("*", count=CountMethod.exact)
            .limit(limit)
            .offset(offset)
            .order("created_at", desc=is_desc)
        )
        if search:
            stmt = stmt.ilike("item_name", f"%{search}%")
        if category_id:
            stmt = stmt.eq("category_id", category_id)
        if created_by:
            stmt = stmt.eq("created_by", created_by)
        if start_date:
            stmt = stmt.gte("created_at", start_date)
        if end_date:
            stmt = stmt.lte("created_at", end_date)

        resp = stmt.execute()

        return (
            [Purchase.model_validate(row) for row in resp.data],
            resp.count if resp.count else 0,
        )

    def get_purchase_by_id(self, purchase_id: str) -> Purchase | None:
        """Retrieve a specific purchase by its ID.

        Args:
            purchase_id: Unique identifier of the purchase

        Returns:
            Purchase: The requested purchase record
        """
        resp = (
            self.client.table(TABLE_NAME)
            .select("*, transformations(*)")
            .eq("id", purchase_id)
            .execute()
        )
        data = resp.data
        if data:
            return Purchase.model_validate(data[0])
        return None

    def create_purchase(self, payload: PurchaseCreate) -> Purchase:
        """Create a new purchase in the database.

        Args:
            payload: Purchase creation data

        Returns:
            Purchase: The newly created purchase record
        """
        data = serialize_for_supabase(payload.model_dump())
        resp = self.client.table(TABLE_NAME).insert(data).execute()
        return Purchase.model_validate(resp.data[0])

    def delete_purchase(self, purchase_id: str) -> None:
        """Delete a purchase from the database.

        Args:
            purchase_id: Unique identifier of the purchase to delete
        """
        self.client.table(TABLE_NAME).delete().eq("id", purchase_id).execute()
