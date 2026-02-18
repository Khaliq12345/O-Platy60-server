"""Product service for business logic."""

from typing import Dict, List
from app.models.product import Product, ProductPayload, ProductCreate, ProductUpdate
from app.db.repositories.product_repository import ProductRepo
from app.core.exception import DatabaseError, ItemNotFoundError


class ProductService:
    def __init__(self) -> None:
        self.repo = ProductRepo()

    def get_products(self, payload: ProductPayload) -> Dict[str, List[Product] | int]:
        """Get all products with optional filters."""
        try:
            products, count = self.repo.list_products(
                limit=payload.limit,
                offset=payload.offset,
                name=payload.name,
                category=payload.category,
                ingredient_id=payload.ingredient_id,
            )
            return {"products": products, "count": count}
        except Exception as e:
            raise DatabaseError("get_products", str(e))

    def get_product(self, product_id: str) -> Product:
        """Get a single product by ID."""
        product = None
        try:
            product = self.repo.get_product_by_id(product_id)
        except Exception as e:
            raise DatabaseError("get_product", str(e))
        if not product:
            raise ItemNotFoundError("get_product", product_id)
        return product

    def create_product(self, payload: ProductCreate) -> Product:
        """Create a new product."""
        try:
            return self.repo.create_product(payload)
        except Exception as e:
            raise DatabaseError("create_product", str(e))

    def update_product(self, product_id: str, payload: ProductUpdate) -> Product:
        """Update an existing product."""
        try:
            self.get_product(product_id)
            product = self.repo.update_product(product_id, payload)
            if not product:
                raise ItemNotFoundError("update_product", product_id)
            return product
        except (DatabaseError, ItemNotFoundError):
            raise
        except Exception as e:
            raise DatabaseError("update_product", str(e))

    def delete_product(self, product_id: str) -> None:
        """Delete a product."""
        try:
            self.get_product(product_id)
            self.repo.delete_product(product_id)
        except (DatabaseError, ItemNotFoundError):
            raise
        except Exception as e:
            raise DatabaseError("delete_product", str(e))
