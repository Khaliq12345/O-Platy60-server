from fastapi import Depends
from typing import Annotated

from app.services.ingredient_service import IngredientService
from app.services.product_service import ProductService
from app.services.purchase_service import PurchaseService
from app.services.category_service import CategoryService
from app.services.transformation_service import TransformationService
from app.services.transformation_step_service import TransformationStepService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.inventory_service import InventoryService

purchase_service_depends = Annotated[PurchaseService, Depends(PurchaseService)]
category_service_depends = Annotated[CategoryService, Depends(CategoryService)]
transformation_service_depends = Annotated[
    TransformationService, Depends(TransformationService)
]
transformation_step_service_depends = Annotated[
    TransformationStepService, Depends(TransformationStepService)
]
user_service_depends = Annotated[UserService, Depends(UserService)]
auth_service_depends = Annotated[AuthService, Depends(AuthService)]
inventory_service_depends = Annotated[InventoryService, Depends(InventoryService)]
ingredient_service_depends = Annotated[IngredientService, Depends(IngredientService)]
product_service_depends = Annotated[ProductService, Depends(ProductService)]
