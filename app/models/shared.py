from datetime import datetime
from typing import Self
from pydantic import BaseModel, Field, model_validator
from enum import Enum


class Order(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class FilterPayload(BaseModel):
    """Base filters for all list endpoints"""

    search: str | None = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, le=100)
    start_date: datetime | None | str = None
    end_date: datetime | None | str = None
    order: Order = Order.DESCENDING

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        self.start_date = (
            self.start_date.isoformat()
            if isinstance(self.start_date, datetime)
            else None
        )
        self.end_date = (
            self.end_date.isoformat() if isinstance(self.end_date, datetime) else None
        )
        return self

    @property
    def offset(self) -> int:
        """Calculates offset automatically"""
        return (self.page - 1) * self.limit

    @property
    def is_desc(self) -> bool:
        """Boolean check for descending order"""
        return self.order == Order.DESCENDING
