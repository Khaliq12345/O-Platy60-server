from typing import List
from uuid import UUID
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.db.repositories.category_repository import CategoryRepo
from app.core.exception import DatabaseError, ItemNotFoundError


class CategoryService:
    def __init__(self) -> None:
        self.repo = CategoryRepo()

    def get_categories(self) -> List[Category]:
        """Get all categories"""
        try:
            categories = self.repo.list_categories()
            return categories
        except Exception as e:
            raise DatabaseError("get_categories", str(e))

    def get_category(self, category_id: UUID) -> Category:
        """Get a single category"""
        category = None
        try:
            category = self.repo.get_category_by_id(category_id)
        except Exception as e:
            raise DatabaseError("get_category", str(e))
        if not category:
            raise ItemNotFoundError("get_category", str(category_id))
        return category

    def create_category(self, payload: CategoryCreate) -> Category:
        """Create a new category"""
        try:
            category = self.repo.create_category(payload)
            return category
        except Exception as e:
            raise DatabaseError("create_category", str(e))

    def update_category(self, category_id: UUID, payload: CategoryUpdate) -> Category:
        """Update an existing category"""
        try:
            category = self.repo.update_category(category_id, payload)
            if not category:
                raise ItemNotFoundError("update_category", str(category_id))
            return category
        except Exception as e:
            raise DatabaseError("update_category", str(e))

    def delete_category(self, category_id: UUID) -> None:
        """Delete a category"""
        try:
            # Check if category exists first
            self.get_category(category_id)
            self.repo.delete_category(category_id)
        except Exception as e:
            raise DatabaseError("delete_category", str(e))