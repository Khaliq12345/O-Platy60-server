from typing import List
from app.models.purchase import Purchase, PurchasePayload
from app.db.repositories.purchase_repository import PurchaseRepo
from app.core.exception import DatabaseError, ItemNotFoundError


class PurchaseService:
    def __init__(self) -> None:
        self.repo = PurchaseRepo()

    def get_purchases(self, payload: PurchasePayload) -> List[Purchase]:
        """Get all purchases with filter or not"""
        try:
            # Date formatting
            start_date = payload.start_date.isoformat() if payload.start_date else None
            end_date = payload.end_date.isoformat() if payload.end_date else None

            # Order formatting
            is_desc = payload.order.value == "desc"

            # Offset formatting
            offset = (payload.page - 1) * payload.limit

            purchases = self.repo.list_purchases(
                start_date=start_date,
                end_date=end_date,
                category_id=payload.category_id,
                limit=payload.limit,
                is_desc=is_desc,
                offset=offset,
            )
            return purchases
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
