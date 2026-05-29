"""Backend tests: policy evaluation unit tests."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.models.policy import Policy, PolicyStatus, PolicyEffect, PolicyType
from app.schemas.policy import PolicyEvaluationRequest
from app.services.policy import PolicyService


def make_policy(effect: PolicyEffect, subjects=None, resources=None) -> Policy:
    p = Policy()
    p.id = uuid4()
    p.name = "test-policy"
    p.policy_type = PolicyType.ACCESS
    p.effect = effect
    p.status = PolicyStatus.ACTIVE
    p.priority = 100
    p.rules = {}
    p.subjects = subjects
    p.resources = resources
    p.is_system = False
    return p


@pytest.mark.asyncio
async def test_evaluate_locally_allow():
    db = AsyncMock()
    allow_policy = make_policy(PolicyEffect.ALLOW, subjects={"roles": ["admin"]})
    db.execute = AsyncMock(return_value=MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[allow_policy])))))

    service = PolicyService(db)
    req = PolicyEvaluationRequest(
        subject={"role": "admin", "id": str(uuid4())},
        resource={"type": "dashboard"},
        action="read",
    )
    result = await service._evaluate_locally(req)
    assert result.allowed is True
    assert result.policy_id == allow_policy.id


@pytest.mark.asyncio
async def test_evaluate_locally_deny_by_policy():
    db = AsyncMock()
    deny_policy = make_policy(PolicyEffect.DENY, subjects={"roles": ["employee"]})
    db.execute = AsyncMock(return_value=MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[deny_policy])))))

    service = PolicyService(db)
    req = PolicyEvaluationRequest(
        subject={"role": "employee"},
        resource={"type": "admin-panel"},
        action="write",
    )
    result = await service._evaluate_locally(req)
    assert result.allowed is False
    assert "Denied by policy" in result.reason


@pytest.mark.asyncio
async def test_evaluate_locally_default_deny():
    """No matching policy → default deny (Zero Trust principle)."""
    db = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))))

    service = PolicyService(db)
    req = PolicyEvaluationRequest(
        subject={"role": "employee"},
        resource={"type": "secret"},
        action="read",
    )
    result = await service._evaluate_locally(req)
    assert result.allowed is False
    assert "default deny" in result.reason


def test_check_subject_role_match():
    db = AsyncMock()
    service = PolicyService(db)
    assert service._check_subject({"roles": ["admin"]}, {"role": "admin"}) is True
    assert service._check_subject({"roles": ["admin"]}, {"role": "employee"}) is False
    assert service._check_subject({}, {"role": "anything"}) is True


def test_check_subject_group_match():
    db = AsyncMock()
    service = PolicyService(db)
    assert service._check_subject({"groups": ["dev"]}, {"groups": ["dev", "ops"]}) is True
    assert service._check_subject({"groups": ["security"]}, {"groups": ["dev"]}) is False


def test_check_resource_type_match():
    db = AsyncMock()
    service = PolicyService(db)
    assert service._check_resource({"types": ["dashboard"]}, {"type": "dashboard"}) is True
    assert service._check_resource({"types": ["admin"]}, {"type": "dashboard"}) is False
    assert service._check_resource({}, {"type": "anything"}) is True
