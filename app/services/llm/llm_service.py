"""LLM service for interactions with model."""

from langchain_ollama import ChatOllama

from app.core.prompt_builder import prompt_builder
from app.services.embeddings.vectorstore import vector_store


class LLMService:
    """
    LLM service.
    Perform allowed operations with model.
    """

    async def create_llm_request(
        self,
        question: str,
        collection_name: str,
    ) -> str:
        """
        Build prompt for LLM model.
        Initially retrieve context from vector db.
        """
        context = await vector_store.retrieve_documents(
            collection_name=collection_name,
            question=question,
        )
        prompt = prompt_builder.create_new_prompt(
            context=context,
            question=question,
        )

        return prompt

    async def invoke_llm(
        self,
        question: str,
        collection_name: str,
    ) -> str:
        """Send prompt to LLM and receive result."""
        prompt = await self.create_llm_request(
            question=question,
            collection_name=collection_name,
        )

        invoke_res = await ChatOllama.ainvoke(
            input=prompt,
        )

        return invoke_res.content
