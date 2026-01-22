from typing import List
from uuid import UUID
from app.models.users import User, UserCreate, UserUpdate
from app.db.repositories.users_repository import UserRepo
from app.core.exception import DatabaseError, ItemNotFoundError


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepo()

    def get_users(self) -> List[User]:
        """Get all users"""
        try:
            users = self.repo.list_users()
            return users
        except Exception as e:
            raise DatabaseError("get_users", str(e))

    def get_user(self, user_id: UUID) -> User:
        """Get a single user"""
        user = None
        try:
            user = self.repo.get_user_by_id(user_id)
        except Exception as e:
            raise DatabaseError("get_user", str(e))
        if not user:
            raise ItemNotFoundError("get_user", str(user_id))
        return user

    def create_user(self, payload: UserCreate) -> User:
        """Create a new user"""
        try:
            user = self.repo.create_user(payload)
            return user
        except Exception as e:
            raise DatabaseError("create_user", str(e))

    def update_user(self, user_id: UUID, payload: UserUpdate) -> User:
        """Update an existing user"""
        try:
            user = self.repo.update_user(user_id, payload)
            if not user:
                raise ItemNotFoundError("update_user", str(user_id))
            return user
        except Exception as e:
            raise DatabaseError("update_user", str(e))

    def delete_user(self, user_id: UUID) -> None:
        """Delete a user"""
        try:
            # Check if user exists first
            self.get_user(user_id)
            self.repo.delete_user(user_id)
        except Exception as e:
            raise DatabaseError("delete_user", str(e))