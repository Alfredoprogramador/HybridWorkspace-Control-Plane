"""SQLAlchemy models for Device management."""
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class DeviceOS(str, PyEnum):
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    IOS = "ios"
    ANDROID = "android"


class DeviceTrustLevel(str, PyEnum):
    TRUSTED = "trusted"
    CONDITIONAL = "conditional"
    UNTRUSTED = "untrusted"
    BLOCKED = "blocked"


class DeviceStatus(str, PyEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    ENROLLED = "enrolled"
    PENDING = "pending"
    REVOKED = "revoked"


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hostname: Mapped[str] = mapped_column(String(255), nullable=False)
    serial_number: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    os_type: Mapped[DeviceOS] = mapped_column(String(20), nullable=False)
    os_version: Mapped[Optional[str]] = mapped_column(String(100))
    agent_version: Mapped[Optional[str]] = mapped_column(String(50))

    # Zero Trust posture
    trust_level: Mapped[DeviceTrustLevel] = mapped_column(
        String(20), default=DeviceTrustLevel.UNTRUSTED
    )
    status: Mapped[DeviceStatus] = mapped_column(String(20), default=DeviceStatus.PENDING)
    is_compliant: Mapped[bool] = mapped_column(Boolean, default=False)
    compliance_score: Mapped[Optional[float]] = mapped_column(Float)

    # Posture details
    disk_encrypted: Mapped[bool] = mapped_column(Boolean, default=False)
    antivirus_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    os_up_to_date: Mapped[bool] = mapped_column(Boolean, default=False)
    firewall_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    screen_lock_enabled: Mapped[bool] = mapped_column(Boolean, default=False)

    # Network
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    tailscale_ip: Mapped[Optional[str]] = mapped_column(String(45))
    mac_address: Mapped[Optional[str]] = mapped_column(String(17))

    # Metadata
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    enrolled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    owner: Mapped[Optional["User"]] = relationship(back_populates="devices")  # noqa: F821
    posture_checks: Mapped[list["PostureCheck"]] = relationship(back_populates="device")


class PostureCheck(Base):
    __tablename__ = "posture_checks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE")
    )
    check_type: Mapped[str] = mapped_column(String(100), nullable=False)
    result: Mapped[bool] = mapped_column(Boolean, nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text)
    raw_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    device: Mapped[Device] = relationship(back_populates="posture_checks")
