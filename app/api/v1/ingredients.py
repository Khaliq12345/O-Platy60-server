"""Ingredient API endpoints.
This module defines REST API endpoints for ingredient management,
including CRUD operations and business logic for ingredients.
"""

from typing import Dict, List
from fastapi import APIRouter, Query, status
from app.api.deps import ingredient_service_depends
from app.models.ingredients import (
    Ingredient,
    IngredientCreate,
    IngredientPayload,
    IngredientUpdate,
)

router: APIRouter = APIRouter(prefix="/v1/ingredients", tags=["ingredients"])


@router.get("/", response_model=Dict[str, List[Ingredient] | int])
def get_ingredients(
    ingredient_service: ingredient_service_depends, payload: IngredientPayload = Query()
) -> Dict[str, List[Ingredient] | int]:
    """Retrieve all ingredients."""
    return ingredient_service.get_ingredients(payload)


@router.get("/{ingredient_id}", response_model=Ingredient)
def get_ingredient(
    ingredient_service: ingredient_service_depends, ingredient_id: str
) -> Ingredient:
    """Retrieve a specific ingredient by ID.

    Args:
        ingredient_id: Unique identifier of the ingredient

    Returns:
        Ingredient: The requested ingredient record
    """
    return ingredient_service.get_ingredient(ingredient_id)


@router.post("/", response_model=Ingredient, status_code=status.HTTP_201_CREATED)
def create_ingredient_endpoint(
    ingredient_service: ingredient_service_depends, payload: IngredientCreate
) -> Ingredient:
    """Create a new ingredient.

    Args:
        payload: Ingredient creation data

    Returns:
        Ingredient: The newly created ingredient
    """
    return ingredient_service.create_ingredient(payload)


@router.put("/{ingredient_id}", response_model=Ingredient)
def update_ingredient_endpoint(
    ingredient_service: ingredient_service_depends,
    ingredient_id: str,
    payload: IngredientUpdate,
) -> Ingredient:
    """Update an existing ingredient.

    Args:
        ingredient_id: Unique identifier of the ingredient to update
        payload: Updated ingredient data

    Returns:
        Ingredient: The updated ingredient
    """
    return ingredient_service.update_ingredient(ingredient_id, payload)


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient_endpoint(
    ingredient_service: ingredient_service_depends, ingredient_id: str
) -> None:
    """Delete an ingredient.

    Args:
        ingredient_id: Unique identifier of the ingredient to delete
    """
    ingredient_service.delete_ingredient(ingredient_id)
