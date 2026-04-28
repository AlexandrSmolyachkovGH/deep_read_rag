"""Interface for Embedding Service."""

from enum import StrEnum
from typing import Callable

from langchain_core.embeddings import Embeddings
from langchain_ollama.embeddings import OllamaEmbeddings

from app.settings.settings import settings


class EmbModel(StrEnum):
    """Allowed models implemented for the service."""
    ollama = "ollama"


def create_ollama() -> OllamaEmbeddings:
    """Create ollama client."""
    return OllamaEmbeddings(
        model=settings.doc_settings.MODEL_TYPE,
        base_url=settings.doc_settings.MODEL_URL,
    )


embedding_models: dict[str, Callable[[], Embeddings]] = {
    "ollama": create_ollama,
}


class EmbCliFactory:
    """Create client for relevant embedding model."""

    def set_model(
        self,
        model: EmbModel,
    ) -> Embeddings:
        """Set embedding model."""
        factory: Callable[[], Embeddings] | None = embedding_models.get(
            model,
            None,
        )

        if not factory:
            raise ValueError("Wrong embedding model")

        return factory()
