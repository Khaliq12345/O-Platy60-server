from typing import List
from uuid import UUID
from app.models.transformation import Transformation, TransformationCreate, TransformationUpdate
from app.db.repositories.transformation_repository import TransformationRepo
from app.core.exception import DatabaseError, ItemNotFoundError


class TransformationService:
    def __init__(self) -> None:
        self.repo = TransformationRepo()

    def get_transformations(self) -> List[Transformation]:
        """Get all transformations"""
        try:
            transformations = self.repo.list_transformations()
            return transformations
        except Exception as e:
            raise DatabaseError("get_transformations", str(e))

    def get_transformation(self, transformation_id: UUID) -> Transformation:
        """Get a single transformation"""
        transformation = None
        try:
            transformation = self.repo.get_transformation_by_id(transformation_id)
        except Exception as e:
            raise DatabaseError("get_transformation", str(e))
        if not transformation:
            raise ItemNotFoundError("get_transformation", str(transformation_id))
        return transformation

    def create_transformation(self, payload: TransformationCreate) -> Transformation:
        """Create a new transformation"""
        try:
            transformation = self.repo.create_transformation(payload)
            return transformation
        except Exception as e:
            raise DatabaseError("create_transformation", str(e))

    def update_transformation(self, transformation_id: UUID, payload: TransformationUpdate) -> Transformation:
        """Update an existing transformation"""
        try:
            transformation = self.repo.update_transformation(transformation_id, payload)
            if not transformation:
                raise ItemNotFoundError("update_transformation", str(transformation_id))
            return transformation
        except Exception as e:
            raise DatabaseError("update_transformation", str(e))

    def delete_transformation(self, transformation_id: UUID) -> None:
        """Delete a transformation"""
        try:
            # Check if transformation exists first
            self.get_transformation(transformation_id)
            self.repo.delete_transformation(transformation_id)
        except Exception as e:
            raise DatabaseError("delete_transformation", str(e))