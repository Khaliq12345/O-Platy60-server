from fastapi import Depends
from typing import Annotated

from app.services.purchase_service import PurchaseService

purchase_service_depends = Annotated[PurchaseService, Depends(PurchaseService)]

