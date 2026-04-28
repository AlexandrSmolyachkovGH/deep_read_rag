"""Document uploading and processing."""
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.settings.settings import settings


async def load_document(
    file_path: str,
    encoding: str = "utf-8",
) -> list[Document]:
    """Upload text file via TextLoader.
    Return list[Document] (Document: text and metadata).
    """
    loader = TextLoader(
        file_path=file_path,
        encoding=encoding,
    )
    documents = await loader.aload()
    return documents


def split_document(
    documents: list[Document]
) -> list[Document]:
    """Split text in document for semantic chunks.
    Use exactly RecursiveCharacterTextSplitter to save context between chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=settings.doc_settings.CHUNK_SIZE,
        chunk_overlap=settings.doc_settings.CHUNK_OVERLAP,
    )

    chunks = text_splitter.split_documents(documents=documents)

    for i, doc in enumerate(chunks):
        doc.metadata["chunk_index"] = i
        source: str | None = doc.metadata.get("source", None)

        if not source:
            file_name: str = "unknown"
        else:
            file_name = Path(source).name

        doc.metadata["file_name"] = file_name

    return chunks
