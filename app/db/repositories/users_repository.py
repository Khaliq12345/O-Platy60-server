"""User repository for database operations.

This module provides data access layer functions for user entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List, Optional

from app.db.supabase import SUPABASE
from app.models.users import User, UserCreate, UserUpdate
from app.services.serialization import serialize_for_supabase

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

    def get_user_by_id(self, user_id: str) -> User | None:
        """Retrieve a specific user by their ID.

        Args:
            user_id: Unique identifier of the user

        Returns:
            User | None: The requested user record or None if not found
        """
        resp = self.client.table(TABLE_NAME).select("*").eq("id", user_id).execute()
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

    def update_user(self, user_id: str, full_name: str = None) -> Optional[dict]:
        """Update user full_name in auth.users metadata and public table."""
        
        if full_name is None:
            return None
        
        # Update public table
        resp = (
            self.client.table(TABLE_NAME)
            .update({"full_name": full_name})
            .eq("id", user_id)
            .execute()
        )

        return resp.data[0] if resp.data else None

    def delete_user(self, user_id: str) -> None:
        """Delete a user from the database.

        Args:
            user_id: Unique identifier of the user to delete

        Note:
            This operation will fail if there are purchases created by this user
            due to foreign key constraints.
        """
        self.client.auth.admin.delete_user(user_id)
        self.client.table(TABLE_NAME).update({"is_deleted": True}).eq("id", user_id).execute()
