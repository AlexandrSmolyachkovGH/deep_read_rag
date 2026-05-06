"""LLM service for interactions with model."""

from langchain_ollama import ChatOllama

from app.core.prompt_builder import prompt_builder
from app.services.embeddings.vectorstore import vector_store
from app.settings.settings import settings


class LLMService:
    """
    LLM service.
    Perform allowed operations with model.
    """

    async def create_llm_request(
        self,
        question: str,
        collection_name: str,
    ) -> tuple[str, list[str]]:
        """
        Build prompt for LLM model.
        Initially retrieve context from vector db.
        """
        context = await vector_store.retrieve_documents(
            collection_name=collection_name,
            question=question,
        )
        sources = list(
            {doc.metadata.get("file_name", "unknown") for doc in context},
        )
        prompt = prompt_builder.create_new_prompt(
            context=context,
            question=question,
        )

        return prompt, sources

    async def invoke_llm(
        self,
        question: str,
        collection_name: str,
    ) -> tuple[str, list[str]]:
        """Send prompt to LLM and receive result."""
        prompt, sources = await self.create_llm_request(
            question=question,
            collection_name=collection_name,
        )

        llm = ChatOllama(
            model=settings.doc_settings.LLM_MODEL,
            base_url=settings.doc_settings.MODEL_URL,
            num_ctx=1024,
        )

        invoke_res = await llm.ainvoke(
            input=prompt,
        )

        return invoke_res.content, sources


llm_service = LLMService()
