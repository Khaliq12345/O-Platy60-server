"""Transformation repository for database operations.

This module provides data access layer functions for transformation entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List
from uuid import UUID
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
        purchase_id: str | None = None,
        limit: int = 20,
        offset: int = 0,
        is_desc: bool = True,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> List[Transformation]:
        """Retrieve all transformations from the database.

        Returns:
            List[Transformation]: List of all transformation records ordered by date (newest first)
        """
        stmt = (
            self.client.table(TABLE_NAME)
            .select("*")
            .limit(limit)
            .offset(offset)
            .order("transformed_at", desc=is_desc)
        )
        if purchase_id:
            stmt = stmt.eq("purchase_id", purchase_id)
        if start_date:
            stmt = stmt.gte("transformed_at", start_date)
        if end_date:
            stmt = stmt.lte("transformed_at", end_date)

        resp = stmt.execute()
        return [Transformation.model_validate(row) for row in resp.data]

    def get_transformation_by_id(self, transformation_id: UUID) -> Transformation | None:
        """Retrieve a specific transformation by its ID.

        Args:
            transformation_id: Unique identifier of the transformation

        Returns:
            Transformation | None: The requested transformation record or None if not found
        """
        resp = (
            self.client.table(TABLE_NAME).select("*").eq("id", str(transformation_id)).execute()
        )
        data = resp.data
        if data:
            return Transformation.model_validate(data[0])
        return None

    def create_transformation(self, payload: TransformationCreate) -> Transformation:
        """Create a new transformation in the database.

        Args:
            payload: Transformation creation data

        Returns:
            Transformation: The newly created transformation record

        Note:
            The purchase_id should reference an existing purchase record.
        """
        data = serialize_for_supabase(payload.model_dump())
        resp = self.client.table(TABLE_NAME).insert(data).execute()
        return Transformation.model_validate(resp.data[0])

    def update_transformation(
        self, transformation_id: UUID, payload: TransformationUpdate
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

    def delete_transformation(self, transformation_id: UUID) -> None:
        """Delete a transformation from the database.

        Args:
            transformation_id: Unique identifier of the transformation to delete

        Note:
            This operation will also delete all associated transformation steps
            due to cascade delete constraints.
        """
        self.client.table(TABLE_NAME).delete().eq("id", str(transformation_id)).execute()
