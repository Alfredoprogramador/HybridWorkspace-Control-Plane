"""Authentication service."""
import uuid
from datetime import datetime, timezone
from typing import Optional

import pyotp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User, UserRole, AuthProvider
from app.schemas.user import UserCreate, TokenResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, data: UserCreate) -> User:
        user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            hashed_password=get_password_hash(data.password),
            role=data.role,
            department=data.department,
            location=data.location,
            auth_provider=AuthProvider.LOCAL,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.get_user_by_username(username)
        if not user or not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        user.last_login_at = datetime.now(timezone.utc)
        await self.db.flush()
        return user

    async def create_tokens(self, user: User) -> TokenResponse:
        from app.core.config import settings

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def refresh_tokens(self, refresh_token: str) -> Optional[TokenResponse]:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                return None
            user_id = uuid.UUID(payload["sub"])
            user = await self.get_user_by_id(user_id)
            if not user or not user.is_active:
                return None
            return await self.create_tokens(user)
        except (ValueError, KeyError):
            return None

    async def setup_mfa(self, user: User) -> str:
        """Generate MFA secret and return provisioning URI."""
        secret = pyotp.random_base32()
        user.mfa_secret = secret
        await self.db.flush()
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=user.email, issuer_name="HybridWorkspace")

    async def verify_mfa(self, user: User, code: str) -> bool:
        if not user.mfa_secret:
            return False
        totp = pyotp.TOTP(user.mfa_secret)
        if totp.verify(code):
            user.is_mfa_enabled = True
            await self.db.flush()
            return True
        return False

    async def get_current_user_from_token(self, token: str) -> Optional[User]:
        try:
            payload = decode_token(token)
            if payload.get("type") != "access":
                return None
            user_id = uuid.UUID(payload["sub"])
            return await self.get_user_by_id(user_id)
        except (ValueError, KeyError):
            return None
