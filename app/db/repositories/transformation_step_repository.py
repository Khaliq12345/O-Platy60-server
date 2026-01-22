"""Transformation step repository for database operations.

This module provides data access layer functions for transformation step entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List
from app.db.supabase import SUPABASE
from app.services.serialization import serialize_for_supabase
from app.models.transformation_step import (
    TransformationStep,
    TransformationStepCreate,
    TransformationStepUpdate,
)


# Database table name for transformation steps
TABLE_NAME: str = "transformation_steps"


class TransformationStepRepo(SUPABASE):
    def __init__(self) -> None:
        super().__init__()

    def list_steps_by_transformation(
        self, 
        transformation_id: str,
        limit: int = 20,
        offset: int = 0,
        is_desc: bool = False,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> List[TransformationStep]:
        """Retrieve all transformation steps for a specific transformation.

        Args:
            transformation_id: Unique identifier of the parent transformation

        Returns:
            List[TransformationStep]: List of transformation steps ordered by creation time
        """
        stmt = (
            self.client.table(TABLE_NAME)
            .select("*")
            .eq("transformation_id", transformation_id)
            .limit(limit)
            .offset(offset)
            .order("created_at", desc=is_desc)
        )
        if start_date:
            stmt = stmt.gte("created_at", start_date)
        if end_date:
            stmt = stmt.lte("created_at", end_date)

        resp = stmt.execute()
        return [TransformationStep.model_validate(row) for row in resp.data]

    def get_step_by_id(self, step_id: str) -> TransformationStep | None:
        """Retrieve a specific transformation step by its ID.

        Args:
            step_id: Unique identifier of the transformation step

        Returns:
            TransformationStep | None: The requested transformation step record or None if not found
        """
        resp = self.client.table(TABLE_NAME).select("*").eq("id", step_id).execute()
        data = resp.data
        if data:
            return TransformationStep.model_validate(data[0])
        return None

    def create_step(self, payload: TransformationStepCreate) -> TransformationStep:
        """Create a new transformation step in the database.

        Args:
            payload: Transformation step creation data

        Returns:
            TransformationStep: The newly created transformation step record
        """
        data = serialize_for_supabase(payload.model_dump())
        resp = self.client.table(TABLE_NAME).insert(data).execute()
        return TransformationStep.model_validate(resp.data[0])

    def update_step(
        self, step_id: str, payload: TransformationStepUpdate
    ) -> TransformationStep | None:
        """Update an existing transformation step in the database.

        Args:
            step_id: Unique identifier of the step to update
            payload: Step update data (only non-None fields will be updated)

        Returns:
            TransformationStep | None: The updated step record, or None if no changes
        """
        update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
        if not update_data:
            return self.get_step_by_id(step_id)

        update_data = serialize_for_supabase(update_data)

        resp = self.client.table(TABLE_NAME).update(update_data).eq("id", step_id).execute()
        data = resp.data
        if data:
            return TransformationStep.model_validate(data[0])
        return None

    def delete_step(self, step_id: str) -> None:
        """Delete a transformation step from the database.

        Args:
            step_id: Unique identifier of the step to delete
        """
        self.client.table(TABLE_NAME).delete().eq("id", step_id).execute()
