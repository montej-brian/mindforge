"""
MINDFORGE — Database Initialization
Setup for SQLAlchemy with async support (aiomysql for MariaDB / aiosqlite for SQLite).
"""
import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings

logger = logging.getLogger(__name__)

# Create async engine
# Note: MariaDB with aiomysql requires the mysql+aiomysql:// protocol
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for providing a database session to FastAPI routes."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Create tables if they don't exist."""
    async with engine.begin() as conn:
        # Import models here to ensure they are registered with Base.metadata
        from models.database_models import TaskDB
        logger.info("Initializing database tables...")
        await conn.run_sync(Base.metadata.create_all)
