"""Postgres settings."""

from pydantic import SecretStr

from app.settings.base import Base


class PgSettings(Base):
    """Postgres settings."""

    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_PORT_OUTER: int
    POSTGRES_PORT_INNER: int

    @property
    def _general_dsn_part(self) -> str:
        """Return general part of PG DSN."""
        return (
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT_INNER}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def pg_async_dsn(self) -> str:
        """Return async Postgres DSN."""
        return f"postgresql+asyncpg://{self._general_dsn_part}"


pg_settings = PgSettings()
