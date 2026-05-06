"""Group up all settings."""

from app.settings.doc_settings import doc_settings
from app.settings.pg import pg_settings
from app.settings.qdrant_settings import qdrant_settings


class Settings:
    """Group up all settings."""

    def __init__(self) -> None:
        """Define all available settings."""
        self.doc_settings = doc_settings
        self.qdrant_settings = qdrant_settings
        self.pg_settings = pg_settings


settings = Settings()
