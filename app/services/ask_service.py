"""Ask service."""

from uuid import UUID

from app.schemes.rag import RagResponse
from app.services.llm.llm_service import llm_service


class AskService:
    """RAG business logic implementation."""

    async def ask_ai(
        self,
        user_id: UUID,
        question: str,
    ) -> RagResponse:
        """
        Ask anything AI.
        If context exists - receive relevant response.
        If context doesn't exist - receive 'context not found' response.
        """
        response, sources = await llm_service.invoke_llm(
            question=question,
            collection_name=str(user_id),
        )

        return RagResponse(
            response=response,
            sources=sources,
        )


ask_service = AskService()
