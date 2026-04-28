"""Vector handling."""

from langchain_core.documents.base import Document
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_qdrant import QdrantVectorStore
from langchain_core.embeddings import Embeddings
from qdrant_client import QdrantClient

from app.settings.settings import settings
from app.services.embeddings.embeddings import EmbCliFactory


class VectorStore:
    """Handler for vectorization, storing and retrieving data."""

    def __init__(self) -> None:
        """VectorStore initialization."""
        self.client = None
        self.embeddings = None

    def _set_embeddings(self) -> Embeddings:
        """Set Embeddings."""
        factory = EmbCliFactory()
        self.embeddings = factory.set_model(
            model=settings.doc_settings.EMBEDDING_MODEL,
        )

        return self.embeddings

    def get_embeddings(self) -> Embeddings:
        """Return Embeddings client.
        If not exists - lazy create initially.
        """
        if not self.embeddings:
            self.embeddings = self._set_embeddings()

        return self.embeddings

    def _set_client(self) -> QdrantClient:
        """Set QdrantClient."""
        self.client = QdrantClient(url=settings.qdrant_settings.qdrant_url)
        return self.client

    def get_client(self) -> QdrantClient:
        """Return Qdrant client.
        If not exists - lazy create initially.
        """
        if not self.client:
            self._set_client()

        return self.client

    def get_vector_store(
        self,
        collection_name: str,
    ) -> QdrantVectorStore:
        """Return QdrantVectorStore with proper settings."""
        return QdrantVectorStore(
            client=self.get_client(),
            embedding=self.get_embeddings(),
            collection_name=collection_name,
        )

    async def vectorize_documents(
        self,
        collection_name: str,
        documents: list[Document],
    ) -> None:
        """Convert document to vector."""
        vector_store: QdrantVectorStore = self.get_vector_store(
            collection_name=collection_name,
        )
        await vector_store.aadd_documents(
            documents=documents
        )

    async def retrieve_documents(
        self,
        collection_name: str,
        question: str,
        search_type: str = "similarity",
    ) -> list[Document]:
        """Retrieve similar documents.
        Compare vectors using search_type = 'similarity' by default.
        """

        vector_store: QdrantVectorStore = self.get_vector_store(
            collection_name=collection_name,
        )
        retriever: VectorStoreRetriever = vector_store.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k": settings.doc_settings.TOP_K,
                "fetch_k": settings.doc_settings.TOP_K * 2,
            }
        )
        docs: list[Document] = await retriever.ainvoke(question)

        return docs

