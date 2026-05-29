"""Health check endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    version: str
    service: str


@router.get("", response_model=HealthResponse)
async def health_check():
    """Service health check."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        service="hwcp-backend",
    )
