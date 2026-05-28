"""Pydantic schemas for Device API."""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.device import DeviceOS, DeviceTrustLevel, DeviceStatus


class DeviceBase(BaseModel):
    name: str = Field(..., max_length=255)
    hostname: str = Field(..., max_length=255)
    os_type: DeviceOS


class DeviceCreate(DeviceBase):
    serial_number: Optional[str] = None
    os_version: Optional[str] = None
    mac_address: Optional[str] = None


class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    os_version: Optional[str] = None
    agent_version: Optional[str] = None
    ip_address: Optional[str] = None
    tailscale_ip: Optional[str] = None


class PostureUpdate(BaseModel):
    disk_encrypted: bool
    antivirus_enabled: bool
    os_up_to_date: bool
    firewall_enabled: bool
    screen_lock_enabled: bool
    os_version: Optional[str] = None


class DeviceResponse(DeviceBase):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    serial_number: Optional[str] = None
    os_version: Optional[str] = None
    agent_version: Optional[str] = None
    trust_level: DeviceTrustLevel
    status: DeviceStatus
    is_compliant: bool
    compliance_score: Optional[float] = None
    disk_encrypted: bool
    antivirus_enabled: bool
    os_up_to_date: bool
    firewall_enabled: bool
    screen_lock_enabled: bool
    ip_address: Optional[str] = None
    tailscale_ip: Optional[str] = None
    mac_address: Optional[str] = None
    owner_id: Optional[uuid.UUID] = None
    last_seen_at: Optional[datetime] = None
    enrolled_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class DeviceList(BaseModel):
    items: list[DeviceResponse]
    total: int
    page: int
    page_size: int


class EnrollmentToken(BaseModel):
    token: str
    device_id: uuid.UUID
    expires_at: datetime
