"""Category repository for database operations.

This module provides data access layer functions for category entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List
from uuid import UUID
from app.db.supabase import SUPABASE
from app.services.serialization import serialize_for_supabase
from app.models.category import Category, CategoryCreate, CategoryUpdate


# Database table name for categories
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
    ) -> List[Category]:
        """Retrieve all categories from the database.

        Returns:
            List[Category]: List of all category records
        """
        stmt = (
            self.client.table(TABLE_NAME)
            .select("*")
            .limit(limit)
            .offset(offset)
            .order("created_at", desc=is_desc)
        )
        if start_date:
            stmt = stmt.gte("created_at", start_date)
        if end_date:
            stmt = stmt.lte("created_at", end_date)

        resp = stmt.execute()
        return [Category.model_validate(row) for row in resp.data]

    def get_category_by_id(self, category_id: UUID) -> Category | None:
        """Retrieve a specific category by its ID.

        Args:
            category_id: Unique identifier of the category

        Returns:
            Category | None: The requested category record or None if not found
        """
        resp = self.client.table(TABLE_NAME).select("*").eq("id", str(category_id)).execute()
        data = resp.data
        if data:
            return Category.model_validate(data[0])
        return None

    def create_category(self, payload: CategoryCreate) -> Category:
        """Create a new category in the database.

        Args:
            payload: Category creation data

        Returns:
            Category: The newly created category record
        """
        data = serialize_for_supabase(payload.model_dump())
        resp = self.client.table(TABLE_NAME).insert(data).execute()
        return Category.model_validate(resp.data[0])

    def update_category(self, category_id: UUID, payload: CategoryUpdate) -> Category | None:
        """Update an existing category in the database.

        Args:
            category_id: Unique identifier of the category to update
            payload: Category update data (only non-None fields will be updated)

        Returns:
            Category | None: The updated category record, or None if no changes
        """
        update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
        if not update_data:
            return self.get_category_by_id(category_id)

        update_data = serialize_for_supabase(update_data)

        resp = (
            self.client.table(TABLE_NAME)
            .update(update_data)
            .eq("id", str(category_id))
            .execute()
        )
        data = resp.data
        if data:
            return Category.model_validate(data[0])
        return None

    def delete_category(self, category_id: UUID) -> None:
        """Delete a category from the database.

        Args:
            category_id: Unique identifier of the category to delete

        Note:
            This operation will fail if there are purchases referencing this category
            due to foreign key constraints.
        """
        self.client.table(TABLE_NAME).delete().eq("id", str(category_id)).execute()
