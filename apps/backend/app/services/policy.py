"""Policy service: evaluate and manage Zero Trust policies."""
import uuid
from typing import Any, Optional

import aiohttp
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.policy import Policy, PolicyAuditLog, PolicyStatus, PolicyEffect
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyEvaluationRequest, PolicyEvaluationResult


class PolicyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_policy(self, policy_id: uuid.UUID) -> Optional[Policy]:
        result = await self.db.execute(select(Policy).where(Policy.id == policy_id))
        return result.scalar_one_or_none()

    async def get_policies(
        self,
        page: int = 1,
        page_size: int = 20,
        policy_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> tuple[list[Policy], int]:
        query = select(Policy)
        count_query = select(func.count(Policy.id))
        if policy_type:
            query = query.where(Policy.policy_type == policy_type)
            count_query = count_query.where(Policy.policy_type == policy_type)
        if status:
            query = query.where(Policy.status == status)
            count_query = count_query.where(Policy.status == status)

        total = (await self.db.execute(count_query)).scalar()
        offset = (page - 1) * page_size
        policies = (
            await self.db.execute(query.order_by(Policy.priority).offset(offset).limit(page_size))
        ).scalars().all()
        return list(policies), total or 0

    async def create_policy(
        self, data: PolicyCreate, created_by_id: Optional[uuid.UUID] = None
    ) -> Policy:
        policy = Policy(**data.model_dump(), created_by_id=created_by_id)
        self.db.add(policy)
        await self.db.flush()
        await self.db.refresh(policy)
        return policy

    async def update_policy(self, policy: Policy, data: PolicyUpdate) -> Policy:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(policy, field, value)
        policy.version += 1
        await self.db.flush()
        await self.db.refresh(policy)
        return policy

    async def delete_policy(self, policy: Policy) -> None:
        await self.db.delete(policy)
        await self.db.flush()

    async def evaluate_policy(
        self, request: PolicyEvaluationRequest
    ) -> PolicyEvaluationResult:
        """Evaluate a policy decision using OPA or local rules."""
        # Try OPA first
        try:
            return await self._evaluate_with_opa(request)
        except Exception:
            # Fallback to local rule evaluation
            return await self._evaluate_locally(request)

    async def _evaluate_with_opa(
        self, request: PolicyEvaluationRequest
    ) -> PolicyEvaluationResult:
        """Send evaluation request to Open Policy Agent."""
        opa_input = {
            "input": {
                "subject": request.subject,
                "resource": request.resource,
                "action": request.action,
                "context": request.context,
            }
        }
        async with aiohttp.ClientSession() as session:
            url = f"{settings.OPA_URL}/v1/data/{settings.OPA_POLICY_PATH}/allow"
            async with session.post(url, json=opa_input, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                resp.raise_for_status()
                result = await resp.json()
                allowed = result.get("result", False)
                return PolicyEvaluationResult(
                    allowed=allowed,
                    reason="OPA policy evaluation",
                )

    async def _evaluate_locally(
        self, request: PolicyEvaluationRequest
    ) -> PolicyEvaluationResult:
        """Local fallback policy evaluation."""
        # Get active policies ordered by priority
        result = await self.db.execute(
            select(Policy)
            .where(Policy.status == PolicyStatus.ACTIVE)
            .order_by(Policy.priority)
        )
        policies = result.scalars().all()

        conditions_met: list[str] = []
        conditions_failed: list[str] = []

        for policy in policies:
            match = self._matches_policy(policy, request)
            if match:
                if policy.effect == PolicyEffect.DENY:
                    return PolicyEvaluationResult(
                        allowed=False,
                        policy_id=policy.id,
                        policy_name=policy.name,
                        reason=f"Denied by policy: {policy.name}",
                        conditions_met=conditions_met,
                        conditions_failed=conditions_failed,
                    )
                elif policy.effect == PolicyEffect.ALLOW:
                    return PolicyEvaluationResult(
                        allowed=True,
                        policy_id=policy.id,
                        policy_name=policy.name,
                        reason=f"Allowed by policy: {policy.name}",
                        conditions_met=conditions_met,
                        conditions_failed=conditions_failed,
                    )

        # Default deny (Zero Trust principle)
        return PolicyEvaluationResult(
            allowed=False,
            reason="No matching allow policy found (default deny)",
        )

    def _matches_policy(self, policy: Policy, request: PolicyEvaluationRequest) -> bool:
        """Check if a policy's subjects and resources match the request."""
        subjects = policy.subjects or {}
        resources = policy.resources or {}

        subject_match = not subjects or self._check_subject(subjects, request.subject)
        resource_match = not resources or self._check_resource(resources, request.resource)

        return subject_match and resource_match

    def _check_subject(self, policy_subjects: dict, request_subject: dict) -> bool:
        """Check if request subject matches policy subject definition."""
        if "roles" in policy_subjects:
            user_role = request_subject.get("role", "")
            if user_role not in policy_subjects["roles"]:
                return False
        if "groups" in policy_subjects:
            user_groups = request_subject.get("groups", [])
            if not any(g in user_groups for g in policy_subjects["groups"]):
                return False
        return True

    def _check_resource(self, policy_resources: dict, request_resource: dict) -> bool:
        """Check if request resource matches policy resource definition."""
        if "types" in policy_resources:
            resource_type = request_resource.get("type", "")
            if resource_type not in policy_resources["types"]:
                return False
        return True
