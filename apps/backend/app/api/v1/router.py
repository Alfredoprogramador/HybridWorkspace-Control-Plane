"""API v1 router aggregation."""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, devices, policies, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(devices.router)
api_router.include_router(policies.router)
