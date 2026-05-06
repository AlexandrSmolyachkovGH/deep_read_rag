"""Prompt builder for LLM."""

from langchain_core.documents.base import Document


class PromptBuilder:
    """Prompt builder for LLM."""

    def __init__(self) -> None:
        """PromptBuilder initialization."""
        self.base_system: dict[str, str] = {
            "system": (
                "Ты помощник.\n"
                "Отвечай грамотно на языке на котором поставлен вопрос.\n"
                "Отвечай только на основе предоставленного контекста.\n"
                "Не придумывай информацию и не добавляй ее извне контекста.\n"
                "Если ответа нет — скажи:\n"
                "\t'Ответ не найден в предоставленных документах'."
            ),
        }
        self.prompt_delimiter: str = "\n\n"
        self.chunk_delimiter: str = "\n---\n"

    def create_new_prompt(
        self,
        context: list[Document],
        question: str,
        system: dict[str, str] | None = None,
    ) -> str:
        """Create structured prompt for LLM."""
        if not system:
            system = self.base_system

        sys_prompt = ""

        for k, v in system.items():
            sys_prompt += f"{k}:\n{v}\n"

        context_prompt = "user:\nКонтекст:\n"
        context_prompt += self.chunk_delimiter

        for doc in context:
            file_name = doc.metadata.get(
                "file_name",
                "unknown",
            )
            context_prompt += f"[Источник: {file_name}]\n{doc.page_content}"

            context_prompt += self.chunk_delimiter

        context_prompt += f"Вопрос:\n{question}"

        return sys_prompt + context_prompt


prompt_builder = PromptBuilder()
