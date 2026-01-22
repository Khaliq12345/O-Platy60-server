"""User repository for database operations.

This module provides data access layer functions for user entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List
from uuid import UUID
from app.db.supabase import SUPABASE
from app.services.serialization import serialize_for_supabase
from app.models.users import User, UserCreate, UserUpdate


# Database table name for users
TABLE_NAME: str = "users"


class UserRepo(SUPABASE):
    def __init__(self) -> None:
        super().__init__()

    def list_users(
        self,
        limit: int = 20,
        offset: int = 0,
        is_desc: bool = True,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> List[User]:
        """Retrieve all users from the database.

        Returns:
            List[User]: List of all user records
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
        return [User.model_validate(row) for row in resp.data]

    def get_user_by_id(self, user_id: UUID) -> User | None:
        """Retrieve a specific user by their ID.

        Args:
            user_id: Unique identifier of the user

        Returns:
            User | None: The requested user record or None if not found
        """
        resp = self.client.table(TABLE_NAME).select("*").eq("id", str(user_id)).execute()
        data = resp.data
        if data:
            return User.model_validate(data[0])
        return None

    def create_user(self, payload: UserCreate) -> User:
        """Create a new user in the database.

        Args:
            payload: User creation data

        Returns:
            User: The newly created user record

        Note:
            Email addresses must be unique across all users.
        """
        data = serialize_for_supabase(payload.model_dump())
        resp = self.client.table(TABLE_NAME).insert(data).execute()
        return User.model_validate(resp.data[0])

    def update_user(self, user_id: UUID, payload: UserUpdate) -> User | None:
        """Update an existing user in the database.

        Args:
            user_id: Unique identifier of the user to update
            payload: User update data (only non-None fields will be updated)

        Returns:
            User | None: The updated user record, or None if no changes
        """
        update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
        if not update_data:
            return self.get_user_by_id(user_id)

        update_data = serialize_for_supabase(update_data)

        resp = self.client.table(TABLE_NAME).update(update_data).eq("id", str(user_id)).execute()
        data = resp.data
        if data:
            return User.model_validate(data[0])
        return None

    def delete_user(self, user_id: UUID) -> None:
        """Delete a user from the database.

        Args:
            user_id: Unique identifier of the user to delete

        Note:
            This operation will fail if there are purchases created by this user
            due to foreign key constraints.
        """
        self.client.table(TABLE_NAME).delete().eq("id", str(user_id)).execute()
