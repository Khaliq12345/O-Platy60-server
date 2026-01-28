from typing import List
from app.db.repositories.transformation_repository import TransformationRepo
from app.db.repositories.transformation_step_repository import TransformationStepRepo
from app.core.exception import DatabaseError, ItemNotFoundError
from app.models.transformation import Transformation, TransformationCreate, TransformationUpdate, TransformationSummary
from app.services.purchase_service import PurchaseService

class TransformationService:
    def __init__(self) -> None:
        self.repo = TransformationRepo()
        self.step_repo = TransformationStepRepo()

    def get_transformations(self) -> List[Transformation]:
        """Get all transformations"""
        try:
            transformations = self.repo.list_transformations()
            return transformations
        except Exception as e:
            raise DatabaseError("get_transformations", str(e))

    def get_transformation(self, transformation_id: str) -> Transformation:
        """Get a single transformation"""
        transformation = None
        try:
            transformation = self.repo.get_transformation_by_id(transformation_id)
        except Exception as e:
            raise DatabaseError("get_transformation", str(e))
        if not transformation:
            raise ItemNotFoundError("get_transformation", transformation_id)
        return transformation

    def create_transformation(self, payload: TransformationCreate) -> Transformation:
        """Create a new transformation"""
        # Verify that the purchase exists
        PurchaseService().get_purchase(payload.purchase_id)

        try:
            transformation = self.repo.create_transformation(payload)
            return transformation
        except Exception as e:
            raise DatabaseError("create_transformation", str(e))

    def update_transformation(self, transformation_id: str, payload: TransformationUpdate) -> Transformation:
        """Update an existing transformation"""
        try:
            transformation = self.repo.update_transformation(transformation_id, payload)
            if not transformation:
                raise ItemNotFoundError("update_transformation", transformation_id)
            return transformation
        except Exception as e:
            raise DatabaseError("update_transformation", str(e))

    def delete_transformation(self, transformation_id: str) -> None:
        """Delete a transformation"""
        # Check if transformation exists first
        self.get_transformation(transformation_id)
        
        try:
            self.repo.delete_transformation(transformation_id)
        except Exception as e:
            raise DatabaseError("delete_transformation", str(e))

    def transformation_summary(self, transformation_id: str) -> TransformationSummary:
        """Get transformation summary with step calculations"""
        try:
            # Get the transformation
            transformation = self.get_transformation(transformation_id)
            
            # Get all steps for this transformation
            steps = self.step_repo.list_steps_by_transformation(transformation_id)
            
            # Calculate totals from steps
            total_portions = sum(step.portions for step in steps)
            total_step_quantity = sum(step.quantity for step in steps)
            step_count = len(steps)
            remaining_quantity = transformation.quantity_usable - total_step_quantity
            
            # Create summary with calculated values
            return TransformationSummary(
                **transformation.model_dump(),
                total_portions=total_portions,
                total_step_quantity=total_step_quantity,
                step_count=step_count,
                remaining_quantity=remaining_quantity
            )
        except Exception as e:
            raise DatabaseError("transformation_summary", str(e))