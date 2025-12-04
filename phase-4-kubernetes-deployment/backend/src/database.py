"""
Database connection and session management for SQLModel.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel
from typing import AsyncGenerator
from .config import settings


import ssl


def get_async_url(url: str) -> str:
    """
    Convert postgresql:// to postgresql+asyncpg:// for async driver.

    Removes sslmode parameter as SSL is configured separately for asyncpg.

    Args:
        url: Database URL with postgresql:// scheme

    Returns:
        str: Database URL with postgresql+asyncpg:// scheme
    """
    # Convert to asyncpg driver
    url = url.replace("postgresql://", "postgresql+asyncpg://")
    # Remove sslmode as asyncpg handles SSL differently
    url = url.replace("?sslmode=require", "").replace("&sslmode=require", "")
    return url


# Create SSL context for asyncpg
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create async database engine
engine = create_async_engine(
    get_async_url(settings.database_url),
    echo=settings.debug,  # Log SQL queries in debug mode
    pool_pre_ping=True,  # Verify connections before using
    connect_args={"ssl": ssl_context},
)

# Create async session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency for FastAPI routes.

    Usage:
        @app.get("/api/tasks")
        async def get_tasks(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with async_session_maker() as session:
        yield session


async def init_db():
    """
    Initialize database tables.

    Creates all SQLModel tables defined in the application.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
