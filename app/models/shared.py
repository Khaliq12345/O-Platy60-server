from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class Order(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class FilterPayload(BaseModel):
    """Filters for the tables"""

    page: int = 1
    limit: int = 20
    start_date: datetime | None = None
    end_date: datetime | None = None
    order: Order = Order.ASCENDING
