"""Device API endpoints."""
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, AdminUser, DB
from app.schemas.device import (
    DeviceCreate,
    DeviceList,
    DeviceResponse,
    DeviceUpdate,
    EnrollmentToken,
    PostureUpdate,
)
from app.services.device import DeviceService

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("", response_model=DeviceList)
async def list_devices(
    db: DB,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: Optional[str] = Query(default=None),
):
    """List devices. Admins see all devices; employees see only their own."""
    from app.models.user import UserRole

    service = DeviceService(db)
    owner_id = None if current_user.role in (UserRole.ADMIN, UserRole.IT_MANAGER, UserRole.SECURITY_ANALYST) else current_user.id
    devices, total = await service.get_devices(page=page, page_size=page_size, owner_id=owner_id, status=status)
    return DeviceList(items=devices, total=total, page=page, page_size=page_size)


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    data: DeviceCreate,
    db: DB,
    current_user: CurrentUser,
):
    """Register a new device."""
    service = DeviceService(db)
    device = await service.create_device(data, owner_id=current_user.id)
    return device


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: uuid.UUID,
    db: DB,
    current_user: CurrentUser,
):
    """Get device details."""
    from app.models.user import UserRole

    service = DeviceService(db)
    device = await service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    if current_user.role == UserRole.EMPLOYEE and device.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return device


@router.patch("/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: uuid.UUID,
    data: DeviceUpdate,
    db: DB,
    current_user: CurrentUser,
):
    """Update device information."""
    from app.models.user import UserRole

    service = DeviceService(db)
    device = await service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    if current_user.role == UserRole.EMPLOYEE and device.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return await service.update_device(device, data)


@router.post("/{device_id}/enroll", response_model=EnrollmentToken)
async def enroll_device(
    device_id: uuid.UUID,
    db: DB,
    current_user: AdminUser,
):
    """Enroll a device and generate its authentication token."""
    service = DeviceService(db)
    device = await service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    device, token = await service.enroll_device(device)
    from datetime import datetime, timezone, timedelta
    return EnrollmentToken(
        token=token,
        device_id=device.id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )


@router.post("/{device_id}/posture", response_model=DeviceResponse)
async def update_device_posture(
    device_id: uuid.UUID,
    posture: PostureUpdate,
    db: DB,
    current_user: CurrentUser,
):
    """Update device security posture (called by device agent)."""
    from app.models.user import UserRole

    service = DeviceService(db)
    device = await service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    if current_user.role == UserRole.EMPLOYEE and device.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return await service.update_posture(device, posture)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: uuid.UUID,
    db: DB,
    current_user: AdminUser,
):
    """Delete/revoke a device."""
    service = DeviceService(db)
    device = await service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    await service.delete_device(device)
