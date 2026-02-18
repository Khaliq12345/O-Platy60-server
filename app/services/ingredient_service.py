from typing import Dict, List
from app.models.ingredients import (
    Ingredient,
    IngredientPayload,
    IngredientCreate,
    IngredientUpdate,
)
from app.db.repositories.ingredient_repository import IngredientRepo
from app.core.exception import DatabaseError, ItemNotFoundError


class IngredientService:
    def __init__(self) -> None:
        self.repo = IngredientRepo()

    def get_ingredients(
        self, payload: IngredientPayload
    ) -> Dict[str, List[Ingredient] | int]:
        """Get all ingredients with optional filters."""
        try:
            ingredients, count = self.repo.list_ingredients(
                limit=payload.limit,
                offset=payload.offset,
                name=payload.name,
                category=payload.category,
            )
            return {"ingredients": ingredients, "count": count}
        except Exception as e:
            raise DatabaseError("get_ingredients", str(e))

    def get_ingredient(self, ingredient_id: str) -> Ingredient:
        """Get a single ingredient by ID."""
        ingredient = None
        try:
            ingredient = self.repo.get_ingredient_by_id(ingredient_id)
        except Exception as e:
            raise DatabaseError("get_ingredient", str(e))
        if not ingredient:
            raise ItemNotFoundError("get_ingredient", ingredient_id)
        return ingredient

    def create_ingredient(self, payload: IngredientCreate) -> Ingredient:
        """Create a new ingredient."""
        try:
            return self.repo.create_ingredient(payload)
        except Exception as e:
            raise DatabaseError("create_ingredient", str(e))

    def update_ingredient(
        self, ingredient_id: str, payload: IngredientUpdate
    ) -> Ingredient:
        """Update an existing ingredient."""
        try:
            self.get_ingredient(ingredient_id)
            ingredient = self.repo.update_ingredient(ingredient_id, payload)
            if not ingredient:
                raise ItemNotFoundError("update_ingredient", ingredient_id)
            return ingredient
        except (DatabaseError, ItemNotFoundError):
            raise
        except Exception as e:
            raise DatabaseError("update_ingredient", str(e))

    def delete_ingredient(self, ingredient_id: str) -> None:
        """Delete an ingredient."""
        try:
            self.get_ingredient(ingredient_id)
            self.repo.delete_ingredient(ingredient_id)
        except (DatabaseError, ItemNotFoundError):
            raise
        except Exception as e:
            raise DatabaseError("delete_ingredient", str(e))
