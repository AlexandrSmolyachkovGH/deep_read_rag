"""Postgres connection file."""

from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.settings.settings import settings


class PgConnHandler:
    """Mange postgres connection."""

    def __init__(
        self,
        pool_size: int = 5,
        max_overflow: int = 10,
        echo: bool = False,
    ) -> None:
        """PG connection init."""
        self.engine = create_async_engine(
            url=settings.pg_settings.pg_async_dsn,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        """Connection pool dispose."""
        await self.engine.dispose()


def create_pg_handler(
    pool_size: int = 5,
    max_overflow: int = 5,
    echo: bool = False,
) -> PgConnHandler:
    """Create PgConnHandler with predefined options."""
    return PgConnHandler(
        pool_size=pool_size,
        max_overflow=max_overflow,
        echo=echo,
    )


async def get_pg_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    """Retrieve a session for main app from the session factory."""
    pg: PgConnHandler = request.app.state.pg

    async with pg.session_factory() as session:
        yield session
