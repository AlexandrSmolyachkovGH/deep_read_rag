"""Qdrant settings."""

from app.settings.base import Base


class QdrantSettings(Base):
    """Qdrant settings."""
    QDRANT_HOST: str
    QDRANT_PORT: int

    @property
    def qdrant_url(self) -> str:
        """Return qdrant url."""
        url = f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

        return url


qdrant_settings = QdrantSettings()
