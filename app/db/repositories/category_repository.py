"""Category repository for database operations."""

from typing import List, Tuple

from postgrest import CountMethod

from app.db.supabase import SUPABASE
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.services.serialization import serialize_for_supabase

TABLE_NAME: str = "categories"


class CategoryRepo(SUPABASE):
    def __init__(self) -> None:
        super().__init__()

    def list_categories(
        self,
        limit: int = 20,
        offset: int = 0,
        is_desc: bool = True,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Tuple[List[Category], int]:
        """Retrieve all categories from the database."""
        stmt = (
            self.client.table(TABLE_NAME)
            .select("*", count=CountMethod.exact)
            .limit(limit)
            .offset(offset)
            .order("created_at", desc=is_desc)
        )
        if start_date:
            stmt = stmt.gte("created_at", start_date)
        if end_date:
            stmt = stmt.lte("created_at", end_date)

        resp = stmt.execute()
        return (
            [Category.model_validate(row) for row in resp.data],
            resp.count if resp.count else 0,
        )

    def get_category_by_id(self, category_id: str) -> Category | None:
        """Retrieve a specific category by its ID."""
        resp = self.client.table(TABLE_NAME).select("*").eq("id", category_id).execute()
        data = resp.data
        if data:
            return Category.model_validate(data[0])
        return None

    def create_category(self, payload: CategoryCreate) -> Category:
        """Create a new category in the database."""
        data = serialize_for_supabase(payload.model_dump())
        resp = self.client.table(TABLE_NAME).insert(data).execute()
        return Category.model_validate(resp.data[0])

    def update_category(
        self, category_id: str, payload: CategoryUpdate
    ) -> Category | None:
        """Update an existing category in the database."""
        update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
        if not update_data:
            return self.get_category_by_id(category_id)

        update_data = serialize_for_supabase(update_data)

        resp = (
            self.client.table(TABLE_NAME)
            .update(update_data)
            .eq("id", category_id)
            .execute()
        )
        data = resp.data
        if data:
            return Category.model_validate(data[0])
        return None

    def delete_category(self, category_id: str) -> None:
        """Delete a category from the database."""
        self.client.table(TABLE_NAME).delete().eq("id", category_id).execute()
