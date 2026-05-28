"""Audit logging middleware."""
import time
import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = structlog.get_logger(__name__)


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Log all API requests for security audit purposes."""

    SENSITIVE_PATHS = {"/api/v1/auth/login", "/api/v1/auth/refresh"}

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        log_data = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", ""),
        }

        # Don't log sensitive request bodies
        if request.url.path not in self.SENSITIVE_PATHS:
            log_data["query_params"] = dict(request.query_params)

        if response.status_code >= 400:
            logger.warning("api_request", **log_data)
        else:
            logger.info("api_request", **log_data)

        return response
