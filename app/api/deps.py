from fastapi import Depends
from typing import Annotated

from app.services.purchase_service import PurchaseService
from app.services.category_service import CategoryService
from app.services.transformation_service import TransformationService
from app.services.transformation_step_service import TransformationStepService
from app.services.user_service import UserService

purchase_service_depends = Annotated[PurchaseService, Depends(PurchaseService)]
category_service_depends = Annotated[CategoryService, Depends(CategoryService)]
transformation_service_depends = Annotated[TransformationService, Depends(TransformationService)]
transformation_step_service_depends = Annotated[TransformationStepService, Depends(TransformationStepService)]
user_service_depends = Annotated[UserService, Depends(UserService)]

