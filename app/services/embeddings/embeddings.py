"""Interface for Embedding Service."""

from collections.abc import Callable
from enum import StrEnum

from langchain_core.embeddings import Embeddings
from langchain_ollama.embeddings import OllamaEmbeddings


class EmbModel(StrEnum):
    """Allowed models implemented for the service."""

    ollama = "ollama"


def create_ollama(
    model: str,
    base_url: str,
) -> OllamaEmbeddings:
    """Create ollama client."""
    return OllamaEmbeddings(
        model=model,
        base_url=base_url,
    )


embedding_models: dict[str, Callable[..., Embeddings]] = {
    "ollama": create_ollama,
}


class EmbCliFactory:
    """Create client for relevant embedding model."""

    def set_model(
        self,
        model: EmbModel,
        model_type: str,
        base_url: str,
    ) -> Embeddings:
        """Set embedding model."""
        factory: Callable[..., Embeddings] | None = embedding_models.get(model)

        if not factory:
            raise ValueError("Wrong embedding model")

        return factory(
            model=model_type,
            base_url=base_url,
        )
