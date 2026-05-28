"""Pydantic schemas for Policy API."""
import uuid
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field

from app.models.policy import PolicyType, PolicyEffect, PolicyStatus


class PolicyBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    policy_type: PolicyType
    effect: PolicyEffect
    priority: int = Field(default=100, ge=1, le=1000)


class PolicyCreate(PolicyBase):
    rules: dict[str, Any]
    subjects: Optional[dict[str, Any]] = None
    resources: Optional[dict[str, Any]] = None
    conditions: Optional[dict[str, Any]] = None
    rego_policy: Optional[str] = None


class PolicyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[PolicyStatus] = None
    priority: Optional[int] = Field(None, ge=1, le=1000)
    rules: Optional[dict[str, Any]] = None
    subjects: Optional[dict[str, Any]] = None
    resources: Optional[dict[str, Any]] = None
    conditions: Optional[dict[str, Any]] = None
    rego_policy: Optional[str] = None


class PolicyResponse(PolicyBase):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    status: PolicyStatus
    rules: dict[str, Any]
    subjects: Optional[dict[str, Any]] = None
    resources: Optional[dict[str, Any]] = None
    conditions: Optional[dict[str, Any]] = None
    rego_policy: Optional[str] = None
    is_system: bool
    version: int
    created_by_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime


class PolicyList(BaseModel):
    items: list[PolicyResponse]
    total: int
    page: int
    page_size: int


class PolicyEvaluationRequest(BaseModel):
    subject: dict[str, Any]
    resource: dict[str, Any]
    action: str
    context: dict[str, Any] = Field(default_factory=dict)


class PolicyEvaluationResult(BaseModel):
    allowed: bool
    policy_id: Optional[uuid.UUID] = None
    policy_name: Optional[str] = None
    reason: Optional[str] = None
    conditions_met: list[str] = Field(default_factory=list)
    conditions_failed: list[str] = Field(default_factory=list)
