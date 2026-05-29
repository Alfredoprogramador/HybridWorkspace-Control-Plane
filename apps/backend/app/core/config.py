"""Application configuration using Pydantic Settings."""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    SERVICE_NAME: str = "hwcp-backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production-use-32-chars-min"
    API_KEY_HEADER: str = "X-API-Key"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_HOSTS: List[str] = ["*"]
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://hwcp:hwcp_dev_password@localhost:5432/hwcp"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET: str = "change-me-in-production-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Zero Trust
    DEVICE_TRUST_EXPIRE_HOURS: int = 24
    CONTINUOUS_VERIFICATION_INTERVAL_MINUTES: int = 15
    MAX_FAILED_VERIFICATIONS: int = 3

    # OPA (Open Policy Agent)
    OPA_URL: str = "http://localhost:8181"
    OPA_POLICY_PATH: str = "hwcp/authz"

    # Tailscale / Headscale
    HEADSCALE_URL: str = "http://localhost:8080"
    HEADSCALE_API_KEY: str = ""

    # Observability
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    PROMETHEUS_METRICS_PATH: str = "/metrics"

    # Email (for notifications)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # SSO Integrations
    MICROSOFT_TENANT_ID: Optional[str] = None
    MICROSOFT_CLIENT_ID: Optional[str] = None
    MICROSOFT_CLIENT_SECRET: Optional[str] = None
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None


settings = Settings()
