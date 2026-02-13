from typing import List, Optional

from pydantic import BaseModel

from app.models.shared import FilterPayload


# INVENTORY TRANSACTION
class InventoryTransactionBase(BaseModel):
    inventory_id: str
    sale: int = 0
    created_at: Optional[str] = None


class InventoryTransactionCreate(InventoryTransactionBase):
    pass


class InventoryTransaction(InventoryTransactionBase):
    id: int
    entry: int = 0


class WeeklyInventorySummary(BaseModel):
    id: int
    start_date: str
    end_date: str
    total_sale: int = 0
    remaining_quantity: int = 0
    manual_inventory: int = 0
    difference: int = 0
    inventory_id: str


# INVENTORY
class InventoryPayload(FilterPayload):
    category_id: str | None = None


class InventoryBase(BaseModel):
    name: str
    initial_quantity: int
    unit: str
    category: Optional[str] = None
    created_at: str


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    initial_quantity: Optional[float] = None
    unit: Optional[str] = None
    category: Optional[str] = None


class DailyTransactionSummary(BaseModel):
    created_at: str
    total_sales: int
    total_quantity: int
    inventory_id: str
    summary_date: str


class InventoryResponse(InventoryBase):
    inventory_id: str
    created_at: str
    daily_transaction_summary: List[DailyTransactionSummary] = []


class InventoryWeeklySummary(BaseModel):
    final_quantity: int
    total_sales: int
    calculated_diff: int


class InventoryWeeklySummaryQuery(BaseModel):
    manual_qty: int
    end_date: str
    inventory_id: str
    start_date: str
