"""Ingredient repository for database operations.
This module provides data access layer functions for ingredient entities,
handling all CRUD operations with the Supabase database.
"""

from typing import List, Tuple
from uuid import UUID
from postgrest import CountMethod
from app.db.supabase import SUPABASE
from app.models.ingredients import (
    Ingredient,
    IngredientCreate,
    IngredientUpdate,
)
from app.services.serialization import serialize_for_supabase

TABLE_NAME: str = "ingredients"


class IngredientRepo(SUPABASE):
    def __init__(self) -> None:
        super().__init__()

    def list_ingredients(
        self,
        limit: int = 20,
        offset: int = 0,
        name: str | None = None,
        category: UUID | None = None,
    ) -> Tuple[List[Ingredient], int]:
        """Retrieve all ingredients from the database.

        Returns:
            Tuple[List[Ingredient], int]: List of ingredients and total count
        """
        stmt = (
            self.client.table(TABLE_NAME)
            .select("*", count=CountMethod.exact)
            .limit(limit)
            .offset(offset)
            .order("created_at", desc=True)
        )

        if name:
            stmt = stmt.ilike("name", f"%{name}%")

        if category:
            stmt = stmt.eq("category", str(category))

        resp = stmt.execute()
        return (
            [Ingredient.model_validate(row) for row in resp.data],
            resp.count if resp.count else 0,
        )

    def get_ingredient_by_id(self, ingredient_id: str) -> Ingredient | None:
        """Retrieve a specific ingredient by its ID.

        Args:
            ingredient_id: Unique identifier of the ingredient

        Returns:
            Ingredient | None: The requested ingredient or None if not found
        """
        resp = (
            self.client.table(TABLE_NAME).select("*").eq("id", ingredient_id).execute()
        )
        data = resp.data
        if data:
            return Ingredient.model_validate(data[0])
        return None

    def create_ingredient(self, payload: IngredientCreate) -> Ingredient:
        """Create a new ingredient in the database.

        Args:
            payload: Ingredient creation data

        Returns:
            Ingredient: The newly created ingredient record
        """
        data = serialize_for_supabase(payload.model_dump())
        resp = self.client.table(TABLE_NAME).insert(data).execute()
        return Ingredient.model_validate(resp.data[0])

    def update_ingredient(
        self, ingredient_id: str, payload: IngredientUpdate
    ) -> Ingredient | None:
        """Update an existing ingredient in the database.

        Args:
            ingredient_id: Unique identifier of the ingredient to update
            payload: Updated ingredient data

        Returns:
            Ingredient: The updated ingredient record
        """
        data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
        if not data:
            return self.get_ingredient_by_id(ingredient_id)
        resp = (
            self.client.table(TABLE_NAME).update(data).eq("id", ingredient_id).execute()
        )
        return Ingredient.model_validate(resp.data[0])

    def delete_ingredient(self, ingredient_id: str) -> None:
        """Delete an ingredient from the database.

        Args:
            ingredient_id: Unique identifier of the ingredient to delete
        """
        self.client.table(TABLE_NAME).delete().eq("id", ingredient_id).execute()
