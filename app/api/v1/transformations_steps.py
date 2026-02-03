"""Transformation step API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, status, Query

from app.models.transformation_step import (
    TransformationStep,
    TransformationStepCreate,
    TransformationStepUpdate,
    TransformationStepPayload,
)
from app.api.deps import transformation_step_service_depends
from app.utils.auth import check_login

router: APIRouter = APIRouter(
    prefix="/v1/transformation-steps",
    tags=["transformation-steps"],
    dependencies=[Depends(check_login)],
)


@router.get("/{transformation_id}/", response_model=List[TransformationStep])
def get_steps_for_transformation(
    transformation_step_service: transformation_step_service_depends,
    transformation_id: str,
    payload: TransformationStepPayload = Query(),
) -> List[TransformationStep]:
    """Retrieve all steps for a specific transformation."""
    return transformation_step_service.get_steps_by_transformation(
        transformation_id, payload
    )


@router.get("/step/{step_id}", response_model=TransformationStep)
def get_step(
    transformation_step_service: transformation_step_service_depends, step_id: str
) -> TransformationStep:
    """Retrieve a specific transformation step by ID."""
    return transformation_step_service.get_step(step_id)


@router.post(
    "/", response_model=TransformationStep, status_code=status.HTTP_201_CREATED
)
def create_step_endpoint(
    transformation_step_service: transformation_step_service_depends,
    payload: TransformationStepCreate,
) -> TransformationStep:
    """Create a new transformation step."""
    return transformation_step_service.create_step(payload)


@router.put("/{step_id}", response_model=TransformationStep)
def update_step_endpoint(
    transformation_step_service: transformation_step_service_depends,
    step_id: str,
    payload: TransformationStepUpdate,
) -> TransformationStep:
    """Update an existing transformation step."""
    return transformation_step_service.update_step(step_id, payload)


@router.delete("/{step_id}")
def delete_step_endpoint(
    transformation_step_service: transformation_step_service_depends, step_id: str
) -> None:
    """Delete a transformation step."""
    transformation_step_service.delete_step(step_id)
