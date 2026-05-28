"""
HybridWorkspace Control Plane - FastAPI Backend
Zero Trust Unified Management Platform
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.telemetry import setup_telemetry
from app.db.session import init_db
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.audit import AuditLogMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    await init_db()
    setup_telemetry(settings.SERVICE_NAME, settings.OTEL_EXPORTER_OTLP_ENDPOINT)
    yield


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="HybridWorkspace Control Plane",
        description="Zero Trust Unified Management Platform for Hybrid Work Environments",
        version="0.1.0",
        docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None,
        openapi_url="/api/openapi.json" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # Security middleware
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(AuditLogMiddleware)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted hosts
    if settings.ENVIRONMENT == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS,
        )

    # Include API router
    app.include_router(api_router, prefix="/api/v1")

    # OpenTelemetry instrumentation
    FastAPIInstrumentor.instrument_app(app)

    return app


app = create_application()
