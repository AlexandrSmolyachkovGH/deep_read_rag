"""Document uploading and processing."""

from uuid import UUID

from langchain_community.document_loaders import TextLoader
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.settings.settings import settings


async def load_document(
    file_path: str,
    encoding: str = "utf-8",
) -> list[Document]:
    """
    Upload text file via TextLoader.
    Return list[Document] (Document: text and metadata).
    """
    loader = TextLoader(
        file_path=file_path,
        encoding=encoding,
    )
    documents = await loader.aload()
    return documents


def split_document(
    documents: list[Document],
    doc_id: UUID,
    user_id: UUID,
    file_name: str,
) -> list[Document]:
    """
    Split text in document for semantic chunks.
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
        doc.metadata["document_id"] = str(doc_id)
        doc.metadata["user_id"] = str(user_id)
        doc.metadata["file_name"] = file_name

    return chunks
