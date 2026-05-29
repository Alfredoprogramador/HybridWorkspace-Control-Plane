"""Authentication API endpoints."""
from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DB
from app.schemas.user import (
    LoginRequest,
    MFAEnableRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: DB):
    """Register a new user."""
    service = AuthService(db)
    if await service.get_user_by_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    if await service.get_user_by_username(data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    return await service.create_user(data)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: DB):
    """Authenticate user and return JWT tokens."""
    service = AuthService(db)
    user = await service.authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await service.create_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, db: DB):
    """Refresh access token using refresh token."""
    service = AuthService(db)
    tokens = await service.refresh_tokens(refresh_token)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    return tokens


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: CurrentUser):
    """Get current authenticated user."""
    return current_user


@router.post("/mfa/setup")
async def setup_mfa(current_user: CurrentUser, db: DB):
    """Enable MFA for the current user."""
    service = AuthService(db)
    provisioning_uri = await service.setup_mfa(current_user)
    return {"provisioning_uri": provisioning_uri}


@router.post("/mfa/verify")
async def verify_mfa(data: MFAEnableRequest, current_user: CurrentUser, db: DB):
    """Verify MFA TOTP code and activate MFA."""
    service = AuthService(db)
    if not await service.verify_mfa(current_user, data.totp_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MFA code",
        )
    return {"message": "MFA enabled successfully"}
