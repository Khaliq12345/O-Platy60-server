"""Transformation repository for database operations.

This module provides data access layer functions for transformation entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List, Tuple

from postgrest import CountMethod
from app.db.supabase import SUPABASE
from app.services.serialization import serialize_for_supabase
from app.models.transformation import (
    Transformation,
    TransformationCreate,
    TransformationUpdate,
)


# Database table name for transformations
TABLE_NAME: str = "transformations"


class TransformationRepo(SUPABASE):
    def __init__(self) -> None:
        super().__init__()

    def list_transformations(
        self,
        search: str | None = None,
        limit: int = 20,
        offset: int = 0,
        is_desc: bool = True,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Tuple[List[Transformation], int]:
        """Retrieve all transformations from the database.

        Returns:
            List[Transformation]: List of all transformation records ordered by date (newest first)
        """
        stmt = (
            self.client.table(TABLE_NAME)
            .select("*", count=CountMethod.exact)
            .limit(limit)
            .offset(offset)
            .order("transformation_date", desc=is_desc)
        )
        if search:
            stmt = stmt.ilike("product_name", f"%{search}%")
        if start_date:
            print(start_date)
            stmt = stmt.gte("transformation_date", start_date)
        if end_date:
            print(end_date)
            stmt = stmt.lte("transformation_date", end_date)

        resp = stmt.execute()
        return (
            [Transformation.model_validate(row) for row in resp.data],
            resp.count if resp.count else 0,
        )

    def get_transformation_by_id(self, transformation_id: str) -> Transformation | None:
        """Retrieve a specific transformation by its ID.

        Args:
            transformation_id: Unique identifier of the transformation

        Returns:
            Transformation | None: The requested transformation record or None if not found
        """
        resp = (
            self.client.table(TABLE_NAME)
            .select("*")
            .eq("id", str(transformation_id))
            .execute()
        )
        data = resp.data
        if data:
            return Transformation.model_validate(data[0])
        return None

    def get_transformation_by_purchase(self, purchase_id: str) -> Transformation | None:
        """Retrieve a specific transformation by its purchase.

        Args:
            purchase_id: Unique identifier of the purchase

        Returns:
            Transformation | None: The requested transformation record or None if not found
        """
        resp = (
            self.client.table(TABLE_NAME)
            .select("*")
            .eq("purchase_id", str(purchase_id))
            .execute()
        )
        data = resp.data
        if data:
            return Transformation.model_validate(data[0])
        return None

    def create_transformation(self, payload: TransformationCreate) -> Transformation:
        """Create a new transformation in the database."""
        data = serialize_for_supabase(payload.model_dump())
        resp = self.client.table(TABLE_NAME).insert(data).execute()
        return Transformation.model_validate(resp.data[0])

    def update_transformation(
        self, transformation_id: str, payload: TransformationUpdate
    ) -> Transformation | None:
        """Update an existing transformation in the database.

        Args:
            transformation_id: Unique identifier of the transformation to update
            payload: Transformation update data (only non-None fields will be updated)

        Returns:
            Transformation | None: The updated transformation record, or None if no changes
        """
        update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
        if not update_data:
            return self.get_transformation_by_id(transformation_id)

        update_data = serialize_for_supabase(update_data)

        resp = (
            self.client.table(TABLE_NAME)
            .update(update_data)
            .eq("id", str(transformation_id))
            .execute()
        )
        data = resp.data
        if data:
            return Transformation.model_validate(data[0])
        return None

    def delete_transformation(self, transformation_id: str) -> None:
        """Delete a transformation from the database.

        Args:
            transformation_id: Unique identifier of the transformation to delete

        Note:
            This operation will also delete all associated transformation steps
            due to cascade delete constraints.
        """
        self.client.table(TABLE_NAME).delete().eq(
            "id", str(transformation_id)
        ).execute()
