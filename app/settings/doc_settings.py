"""Document settings."""

from app.services.embeddings.embeddings import EmbModel
from app.settings.base import Base


class DocumentSettings(Base):
    """Document settings."""

    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    EMBEDDING_MODEL: EmbModel
    MODEL_URL: str
    MODEL_TYPE: str
    TOP_K: int


doc_settings = DocumentSettings()
