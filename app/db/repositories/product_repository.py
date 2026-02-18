"""Product repository for database operations."""

from typing import List, Tuple
from uuid import UUID
from postgrest import CountMethod
from app.db.supabase import SUPABASE
from app.models.product import Product, ProductCreate, ProductUpdate
from app.services.serialization import serialize_for_supabase

TABLE_NAME: str = "products"


class ProductRepo(SUPABASE):
    def __init__(self) -> None:
        super().__init__()

    def list_products(
        self,
        limit: int = 20,
        offset: int = 0,
        name: str | None = None,
        category: UUID | None = None,
        ingredient_id: UUID | None = None,
    ) -> Tuple[List[Product], int]:
        stmt = (
            self.client.table(TABLE_NAME)
            .select("*, ingredients(*)", count=CountMethod.exact)
            .limit(limit)
            .offset(offset)
            .order("created_at", desc=True)
        )

        if name:
            stmt = stmt.ilike("name", f"%{name}%")
        if category:
            stmt = stmt.eq("category", str(category))
        if ingredient_id:
            stmt = stmt.eq("ingredient_id", str(ingredient_id))

        resp = stmt.execute()
        return (
            [Product.model_validate(row) for row in resp.data],
            resp.count if resp.count else 0,
        )

    def get_product_by_id(self, product_id: str) -> Product | None:
        resp = (
            self.client.table(TABLE_NAME)
            .select("*")
            .eq("product_id", product_id)
            .execute()
        )
        data = resp.data
        if data:
            return Product.model_validate(data[0])
        return None

    def create_product(self, payload: ProductCreate) -> Product:
        data = serialize_for_supabase(payload.model_dump())
        resp = self.client.table(TABLE_NAME).insert(data).execute()
        return Product.model_validate(resp.data[0])

    def update_product(self, product_id: str, payload: ProductUpdate) -> Product | None:
        data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
        if not data:
            return self.get_product_by_id(product_id)
        resp = (
            self.client.table(TABLE_NAME)
            .update(data)
            .eq("product_id", product_id)
            .execute()
        )
        return Product.model_validate(resp.data[0])

    def delete_product(self, product_id: str) -> None:
        self.client.table(TABLE_NAME).delete().eq("product_id", product_id).execute()
