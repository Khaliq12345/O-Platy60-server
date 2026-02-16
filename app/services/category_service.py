from typing import List

from typing_extensions import Dict

from app.core.exception import DatabaseError, ItemNotFoundError
from app.db.repositories.category_repository import CategoryRepo
from app.models.category import (
    Category,
    CategoryCreate,
    CategoryPayload,
    CategoryUpdate,
)


class CategoryService:
    def __init__(self) -> None:
        self.repo = CategoryRepo()

    def get_categories(
        self, payload: CategoryPayload
    ) -> Dict[str, List[Category] | int]:
        """Get all categories with filters"""
        try:
            start_date = payload.start_date.isoformat() if payload.start_date else None
            end_date = payload.end_date.isoformat() if payload.end_date else None
            is_desc = payload.order.value == "desc"
            offset = (payload.page - 1) * payload.limit

            categories, count = self.repo.list_categories(
                limit=payload.limit,
                offset=offset,
                is_desc=is_desc,
                start_date=start_date,
                end_date=end_date,
            )
            return {"categories": categories, "count": count}
        except Exception as e:
            raise DatabaseError("get_categories", str(e))

    def get_category(self, category_id: str) -> Category:
        """Get a single category"""
        category = None
        try:
            category = self.repo.get_category_by_id(category_id)
        except Exception as e:
            raise DatabaseError("get_category", str(e))
        if not category:
            raise ItemNotFoundError("get_category", category_id)
        return category

    def create_category(self, payload: CategoryCreate) -> Category:
        """Create a new category"""
        try:
            category = self.repo.create_category(payload)
            return category
        except Exception as e:
            raise DatabaseError("create_category", str(e))

    def update_category(self, category_id: str, payload: CategoryUpdate) -> Category:
        """Update an existing category"""
        try:
            category = self.repo.update_category(category_id, payload)
            if not category:
                raise ItemNotFoundError("update_category", category_id)
            return category
        except Exception as e:
            raise DatabaseError("update_category", str(e))

    def delete_category(self, category_id: str) -> None:
        """Delete a category"""
        try:
            self.get_category(category_id)
            self.repo.delete_category(category_id)
        except Exception as e:
            raise DatabaseError("delete_category", str(e))
