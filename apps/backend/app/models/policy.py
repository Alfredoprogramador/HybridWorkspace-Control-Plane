"""SQLAlchemy models for Policy management."""
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class PolicyType(str, PyEnum):
    ACCESS = "access"
    DEVICE_COMPLIANCE = "device_compliance"
    NETWORK = "network"
    DATA_PROTECTION = "data_protection"
    BEHAVIORAL = "behavioral"


class PolicyEffect(str, PyEnum):
    ALLOW = "allow"
    DENY = "deny"
    CONDITIONAL = "conditional"


class PolicyStatus(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    policy_type: Mapped[PolicyType] = mapped_column(String(30), nullable=False)
    effect: Mapped[PolicyEffect] = mapped_column(String(20), nullable=False)
    status: Mapped[PolicyStatus] = mapped_column(String(20), default=PolicyStatus.DRAFT)
    priority: Mapped[int] = mapped_column(Integer, default=100)

    # Policy rules as JSON (OPA-compatible)
    rules: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Conditions: who, what, where, when
    subjects: Mapped[Optional[dict]] = mapped_column(JSONB)   # users, groups, roles
    resources: Mapped[Optional[dict]] = mapped_column(JSONB)  # what resources
    conditions: Mapped[Optional[dict]] = mapped_column(JSONB) # when/where applicable

    # OPA policy content (Rego)
    rego_policy: Mapped[Optional[str]] = mapped_column(Text)

    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    version: Mapped[int] = mapped_column(Integer, default=1)

    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    audit_logs: Mapped[list["PolicyAuditLog"]] = relationship(back_populates="policy")


class PolicyAuditLog(Base):
    __tablename__ = "policy_audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policies.id", ondelete="CASCADE"),
        nullable=False,
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    actor_email: Mapped[Optional[str]] = mapped_column(String(255))
    changes: Mapped[Optional[dict]] = mapped_column(JSONB)
    decision: Mapped[Optional[str]] = mapped_column(String(20))
    context: Mapped[Optional[dict]] = mapped_column(JSONB)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    policy: Mapped[Policy] = relationship(back_populates="audit_logs")
