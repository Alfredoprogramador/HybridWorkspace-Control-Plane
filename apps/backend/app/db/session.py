"""Database session and initialization."""
from __future__ import annotations

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

_engine: Optional[AsyncEngine] = None
_AsyncSessionLocal: Optional[async_sessionmaker[AsyncSession]] = None


def get_engine() -> AsyncEngine:
    """Return (creating lazily) the shared async engine."""
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            settings.DATABASE_URL,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            echo=settings.DEBUG,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return (creating lazily) the shared session factory."""
    global _AsyncSessionLocal
    if _AsyncSessionLocal is None:
        _AsyncSessionLocal = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _AsyncSessionLocal


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


async def init_db() -> None:
    """Initialize database tables."""
    async with get_engine().begin() as conn:
        # In production, use Alembic migrations instead
        from app.models import device, policy, user  # noqa: F401
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """FastAPI dependency for database session."""
    async with get_session_factory()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
