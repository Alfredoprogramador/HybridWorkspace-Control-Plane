"""Device management service."""
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import Device, PostureCheck, DeviceTrustLevel, DeviceStatus
from app.schemas.device import DeviceCreate, DeviceUpdate, PostureUpdate
from app.core.security import create_device_token


class DeviceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_device(self, device_id: uuid.UUID) -> Optional[Device]:
        result = await self.db.execute(select(Device).where(Device.id == device_id))
        return result.scalar_one_or_none()

    async def get_devices(
        self,
        page: int = 1,
        page_size: int = 20,
        owner_id: Optional[uuid.UUID] = None,
        status: Optional[str] = None,
    ) -> tuple[list[Device], int]:
        query = select(Device)
        count_query = select(func.count(Device.id))

        if owner_id:
            query = query.where(Device.owner_id == owner_id)
            count_query = count_query.where(Device.owner_id == owner_id)
        if status:
            query = query.where(Device.status == status)
            count_query = count_query.where(Device.status == status)

        total = (await self.db.execute(count_query)).scalar()
        offset = (page - 1) * page_size
        devices = (
            await self.db.execute(query.offset(offset).limit(page_size))
        ).scalars().all()

        return list(devices), total or 0

    async def create_device(
        self, data: DeviceCreate, owner_id: Optional[uuid.UUID] = None
    ) -> Device:
        device = Device(
            **data.model_dump(),
            owner_id=owner_id,
            status=DeviceStatus.PENDING,
            trust_level=DeviceTrustLevel.UNTRUSTED,
        )
        self.db.add(device)
        await self.db.flush()
        await self.db.refresh(device)
        return device

    async def update_device(self, device: Device, data: DeviceUpdate) -> Device:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(device, field, value)
        await self.db.flush()
        await self.db.refresh(device)
        return device

    async def enroll_device(self, device: Device) -> tuple[Device, str]:
        """Enroll device and return enrollment token."""
        device.status = DeviceStatus.ENROLLED
        device.enrolled_at = datetime.now(timezone.utc)
        token = create_device_token(str(device.id))
        await self.db.flush()
        return device, token

    async def update_posture(self, device: Device, posture: PostureUpdate) -> Device:
        """Update device posture and recalculate trust level."""
        device.disk_encrypted = posture.disk_encrypted
        device.antivirus_enabled = posture.antivirus_enabled
        device.os_up_to_date = posture.os_up_to_date
        device.firewall_enabled = posture.firewall_enabled
        device.screen_lock_enabled = posture.screen_lock_enabled
        if posture.os_version:
            device.os_version = posture.os_version
        device.last_seen_at = datetime.now(timezone.utc)

        # Calculate compliance score
        checks = [
            posture.disk_encrypted,
            posture.antivirus_enabled,
            posture.os_up_to_date,
            posture.firewall_enabled,
            posture.screen_lock_enabled,
        ]
        score = sum(1 for c in checks if c) / len(checks) * 100
        device.compliance_score = score
        device.is_compliant = score >= 80.0

        # Update trust level based on posture
        if score >= 90:
            device.trust_level = DeviceTrustLevel.TRUSTED
        elif score >= 60:
            device.trust_level = DeviceTrustLevel.CONDITIONAL
        else:
            device.trust_level = DeviceTrustLevel.UNTRUSTED

        # Record posture check
        check = PostureCheck(
            device_id=device.id,
            check_type="full_posture",
            result=device.is_compliant,
            details=f"Compliance score: {score:.1f}%",
            raw_data=posture.model_dump(),
        )
        self.db.add(check)
        await self.db.flush()
        await self.db.refresh(device)
        return device

    async def delete_device(self, device: Device) -> None:
        await self.db.delete(device)
        await self.db.flush()
