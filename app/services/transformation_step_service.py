from typing import List
from app.models.transformation_step import TransformationStep, TransformationStepCreate, TransformationStepUpdate, TransformationStepPayload
from app.db.repositories.transformation_step_repository import TransformationStepRepo
from app.core.exception import DatabaseError, ItemNotFoundError


class TransformationStepService:
    def __init__(self) -> None:
        self.repo = TransformationStepRepo()

    def get_steps_by_transformation(self, transformation_id: str, payload: TransformationStepPayload) -> List[TransformationStep]:
        """Get all transformation steps for a specific transformation"""
        try:
            start_date = payload.start_date.isoformat() if payload.start_date else None
            end_date = payload.end_date.isoformat() if payload.end_date else None
            is_desc = payload.order.value == "desc"
            offset = (payload.page - 1) * payload.limit
            
            steps = self.repo.list_steps_by_transformation(
                transformation_id=transformation_id,
                limit=payload.limit,
                offset=offset,
                is_desc=is_desc,
                start_date=start_date,
                end_date=end_date,
            )
            return steps
        except Exception as e:
            raise DatabaseError("get_steps_by_transformation", str(e))

    def get_step(self, step_id: str) -> TransformationStep:
        """Get a single transformation step"""
        step = None
        try:
            step = self.repo.get_step_by_id(step_id)
        except Exception as e:
            raise DatabaseError("get_step", str(e))
        if not step:
            raise ItemNotFoundError("get_step", step_id)
        return step

    def create_step(self, payload: TransformationStepCreate) -> TransformationStep:
        """Create a new transformation step"""
        try:
            step = self.repo.create_step(payload)
            return step
        except Exception as e:
            raise DatabaseError("create_step", str(e))

    def update_step(self, step_id: str, payload: TransformationStepUpdate) -> TransformationStep:
        """Update an existing transformation step"""
        try:
            step = self.repo.update_step(step_id, payload)
            if not step:
                raise ItemNotFoundError("update_step", step_id)
            return step
        except Exception as e:
            raise DatabaseError("update_step", str(e))

    def delete_step(self, step_id: str) -> None:
        """Delete a transformation step"""
        try:
            # Check if step exists first
            self.get_step(step_id)
            self.repo.delete_step(step_id)
        except Exception as e:
            raise DatabaseError("delete_step", str(e))