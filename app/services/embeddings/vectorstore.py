"""Vector handling."""

import asyncio
import uuid

from langchain_core.documents.base import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.services.embeddings.embeddings import EmbCliFactory
from app.settings.settings import settings


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
            model_type=settings.doc_settings.MODEL_TYPE,
            base_url=settings.doc_settings.MODEL_URL,
        )

        return self.embeddings

    def get_embeddings(self) -> Embeddings:
        """
        Return Embeddings client.
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
        """
        Return Qdrant client.
        If not exists - lazy create initially.
        """
        if not self.client:
            self._set_client()

        return self.client

    def collection_ensure(
        self,
        collection_name: str,
    ) -> None:
        """Check collection. Create new if collection not found."""
        client = self.get_client()
        collections = client.get_collections().collections
        names = [c.name for c in collections]

        if collection_name not in names:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=settings.doc_settings.EMBEDDING_SIZE,
                    distance=Distance.COSINE,
                ),
            )

    async def async_coll_ensure(
        self,
        collection_name: str,
    ) -> None:
        """Async wrapper for collection_ensure."""
        await asyncio.to_thread(
            self.collection_ensure,
            collection_name=collection_name,
        )

    async def _embed_documents_batch(
        self,
        documents: list[Document],
    ) -> tuple[list[list[float]], list[dict]]:
        """Batch embedding for documents."""
        embeddings = self.get_embeddings()

        texts = [doc.page_content for doc in documents]
        metadata = [doc.metadata for doc in documents]

        vectors = await asyncio.to_thread(
            embeddings.embed_documents,
            texts,
        )

        return vectors, metadata

    async def get_vector_store(
        self,
        collection_name: str,
    ) -> QdrantVectorStore:
        """Return QdrantVectorStore with proper settings."""
        await self.async_coll_ensure(
            collection_name=collection_name,
        )

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
        await self.get_vector_store(
            collection_name=collection_name,
        )

        client = self.get_client()
        BATCH_SIZE = 32

        for i in range(0, len(documents), BATCH_SIZE):
            batch = documents[i : i + BATCH_SIZE]

            vectors, _ = await self._embed_documents_batch(batch)

            points = [
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "page_content": doc.page_content,
                        "metadata": doc.metadata,
                    },
                )
                for vector, doc in zip(vectors, batch, strict=True)
            ]

            await asyncio.to_thread(
                client.upsert,
                collection_name=collection_name,
                points=points,
            )

    async def retrieve_documents(
        self,
        collection_name: str,
        question: str,
        search_type: str = "similarity",
    ) -> list[Document]:
        """
        Retrieve similar documents.
        Compare vectors using search_type = 'similarity' by default.
        """
        vector_store: QdrantVectorStore = await self.get_vector_store(
            collection_name=collection_name,
        )
        retriever: VectorStoreRetriever = vector_store.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k": settings.doc_settings.TOP_K,
            },
        )
        docs: list[Document] = await retriever.ainvoke(question)

        return docs


vector_store = VectorStore()
