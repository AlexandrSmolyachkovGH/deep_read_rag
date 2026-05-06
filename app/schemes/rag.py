"""RAG schemes."""

from pydantic import (
    BaseModel,
)


class RagResponse(BaseModel):
    """RAG response scheme."""

    response: str
    sources: list[str]
