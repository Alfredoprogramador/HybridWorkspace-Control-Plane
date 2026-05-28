"""Pydantic schemas for User API."""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole, AuthProvider


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None
    role: UserRole = UserRole.EMPLOYEE
    department: Optional[str] = None
    location: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=12)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    auth_provider: AuthProvider
    is_active: bool
    is_mfa_enabled: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime


class UserList(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class MFAEnableRequest(BaseModel):
    totp_code: str = Field(..., min_length=6, max_length=6)
