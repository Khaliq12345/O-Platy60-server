"""Product API endpoints."""

from typing import Dict, List
from fastapi import APIRouter, Query, status
from app.api.deps import product_service_depends
from app.models.product import (
    Product,
    ProductCreate,
    ProductTransactionPayload,
    ProductTransactionResponse,
    ProductUpdate,
    ProductPayload,
)

router: APIRouter = APIRouter(prefix="/v1/products", tags=["products"])


@router.get("/", response_model=Dict[str, List[Product] | int])
def get_products(
    product_service: product_service_depends, payload: ProductPayload = Query()
) -> Dict[str, List[Product] | int]:
    """Retrieve all products."""
    return product_service.get_products(payload)


@router.get("/{product_id}", response_model=Product)
def get_product(product_service: product_service_depends, product_id: str) -> Product:
    """Retrieve a specific product by ID."""
    return product_service.get_product(product_id)


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(
    product_service: product_service_depends, payload: ProductCreate
) -> Product:
    """Create a new product."""
    return product_service.create_product(payload)


@router.put("/{product_id}", response_model=Product)
def update_product_endpoint(
    product_service: product_service_depends,
    product_id: str,
    payload: ProductUpdate,
) -> Product:
    """Update an existing product."""
    return product_service.update_product(product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(
    product_service: product_service_depends, product_id: str
) -> None:
    """Delete a product."""
    product_service.delete_product(product_id)


@router.post("/transaction/summary")
def delete_product_transaction_summary(
    product_service: product_service_depends, payload: ProductTransactionPayload
) -> Dict:
    """Get product transaction summary"""
    return product_service.get_product_transaction_summary(payload)
