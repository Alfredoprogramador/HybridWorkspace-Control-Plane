"""Policy API endpoints."""
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, AdminUser, DB
from app.schemas.policy import (
    PolicyCreate,
    PolicyEvaluationRequest,
    PolicyEvaluationResult,
    PolicyList,
    PolicyResponse,
    PolicyUpdate,
)
from app.services.policy import PolicyService

router = APIRouter(prefix="/policies", tags=["policies"])


@router.get("", response_model=PolicyList)
async def list_policies(
    db: DB,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    policy_type: Optional[str] = Query(default=None),
    policy_status: Optional[str] = Query(default=None, alias="status"),
):
    service = PolicyService(db)
    policies, total = await service.get_policies(
        page=page, page_size=page_size,
        policy_type=policy_type, status=policy_status,
    )
    return PolicyList(items=policies, total=total, page=page, page_size=page_size)


@router.post("", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    data: PolicyCreate,
    db: DB,
    current_user: AdminUser,
):
    service = PolicyService(db)
    return await service.create_policy(data, created_by_id=current_user.id)


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    policy_id: uuid.UUID,
    db: DB,
    current_user: CurrentUser,
):
    service = PolicyService(db)
    policy = await service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy


@router.patch("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: uuid.UUID,
    data: PolicyUpdate,
    db: DB,
    current_user: AdminUser,
):
    service = PolicyService(db)
    policy = await service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    if policy.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System policies cannot be modified",
        )
    return await service.update_policy(policy, data)


@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    policy_id: uuid.UUID,
    db: DB,
    current_user: AdminUser,
):
    service = PolicyService(db)
    policy = await service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    if policy.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System policies cannot be deleted",
        )
    await service.delete_policy(policy)


@router.post("/evaluate", response_model=PolicyEvaluationResult)
async def evaluate_policy(
    request: PolicyEvaluationRequest,
    db: DB,
    current_user: CurrentUser,
):
    """Evaluate a Zero Trust policy decision."""
    service = PolicyService(db)
    return await service.evaluate_policy(request)
