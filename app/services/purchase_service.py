from typing import Dict, List
from app.models.purchase import (
    Purchase,
    PurchasePayload,
    PurchaseCreate,
)
from app.db.repositories.purchase_repository import PurchaseRepo
from app.db.repositories.transformation_repository import TransformationRepo
from app.core.exception import DatabaseError, ItemNotFoundError, ValidationError


class PurchaseService:
    def __init__(self) -> None:
        self.repo = PurchaseRepo()
        self.transformation_repo = TransformationRepo()

    def get_purchases(
        self, payload: PurchasePayload
    ) -> Dict[str, List[Purchase] | int]:
        """Get all purchases with filter or not"""
        try:
            purchases, count = self.repo.list_purchases(
                search=payload.search,
                limit=payload.limit,
                offset=payload.offset,
                is_desc=payload.is_desc,
                start_date=(
                    payload.start_date if isinstance(payload.start_date, str) else None
                ),
                end_date=(
                    payload.end_date if isinstance(payload.end_date, str) else None
                ),
                category_id=payload.category_id,
                created_by=payload.created_by,
                ingredient=payload.ingredient,
            )
            return {"purchases": purchases, "count": count}
        except Exception as e:
            raise DatabaseError("get_purchases", str(e))

    def get_purchase(self, purchase_id: str) -> Purchase:
        """Get a single purchase"""
        purchase = None
        try:
            purchase = self.repo.get_purchase_by_id(purchase_id)
        except Exception as e:
            raise DatabaseError("get_purchase", str(e))
        if not purchase:
            raise ItemNotFoundError("get_purchase", purchase_id)
        return purchase

    def create_purchase(self, payload: PurchaseCreate) -> Purchase:
        """Create a new purchase"""
        if payload.quantity * payload.price_per_unit != payload.total_price:
            raise ValidationError(
                "create_purchase",
                "total_price must be equal to quantity * price_per_unit",
            )

        try:
            purchase = self.repo.create_purchase(payload)
            return purchase
        except Exception as e:
            raise DatabaseError("create_purchase", str(e))

    def delete_purchase(self, purchase_id: str) -> None:
        """Delete a purchase"""
        try:
            # Check if purchase exists first
            self.get_purchase(purchase_id)
            self.repo.delete_purchase(purchase_id)
        except Exception as e:
            raise DatabaseError("delete_purchase", str(e))
