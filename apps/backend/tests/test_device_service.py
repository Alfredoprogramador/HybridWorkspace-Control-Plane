"""Backend tests: device posture and trust level calculation."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.models.device import Device, DeviceOS, DeviceStatus, DeviceTrustLevel
from app.schemas.device import DeviceCreate, PostureUpdate
from app.services.device import DeviceService


def make_device() -> Device:
    d = Device()
    d.id = uuid4()
    d.name = "test-device"
    d.hostname = "test-host"
    d.os_type = DeviceOS.LINUX
    d.status = DeviceStatus.ENROLLED
    d.trust_level = DeviceTrustLevel.UNTRUSTED
    d.disk_encrypted = False
    d.antivirus_enabled = False
    d.os_up_to_date = False
    d.firewall_enabled = False
    d.screen_lock_enabled = False
    return d


@pytest.mark.asyncio
async def test_posture_update_trusted():
    db = AsyncMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    db.add = MagicMock()

    service = DeviceService(db)
    device = make_device()
    posture = PostureUpdate(
        disk_encrypted=True,
        antivirus_enabled=True,
        os_up_to_date=True,
        firewall_enabled=True,
        screen_lock_enabled=True,
    )
    updated = await service.update_posture(device, posture)
    assert updated.trust_level == DeviceTrustLevel.TRUSTED
    assert updated.compliance_score == 100.0
    assert updated.is_compliant is True


@pytest.mark.asyncio
async def test_posture_update_conditional():
    db = AsyncMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    db.add = MagicMock()

    service = DeviceService(db)
    device = make_device()
    posture = PostureUpdate(
        disk_encrypted=True,
        antivirus_enabled=True,
        os_up_to_date=True,
        firewall_enabled=False,
        screen_lock_enabled=False,
    )
    updated = await service.update_posture(device, posture)
    assert updated.trust_level == DeviceTrustLevel.CONDITIONAL
    assert updated.compliance_score == 60.0
    assert updated.is_compliant is False


@pytest.mark.asyncio
async def test_posture_update_untrusted():
    db = AsyncMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    db.add = MagicMock()

    service = DeviceService(db)
    device = make_device()
    posture = PostureUpdate(
        disk_encrypted=True,
        antivirus_enabled=False,
        os_up_to_date=False,
        firewall_enabled=False,
        screen_lock_enabled=False,
    )
    updated = await service.update_posture(device, posture)
    assert updated.trust_level == DeviceTrustLevel.UNTRUSTED
    assert updated.compliance_score == 20.0
    assert updated.is_compliant is False
