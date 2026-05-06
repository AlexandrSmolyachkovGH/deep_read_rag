"""Document's service."""

import asyncio
from pathlib import Path
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.custom_exceptions import (
    RepositoryException,
    ServiceException,
)
from app.core.temp_file_handler.file_handler import file_handler
from app.models.documents import Document
from app.repositories.documents import doc_repo
from app.schemes.documents import (
    CreateDocReq,
)
from app.services.doc_uploading import (
    load_document,
    split_document,
)
from app.services.embeddings.vectorstore import vector_store


class DocService:
    """Document service."""

    async def create_doc(
        self,
        create_data: CreateDocReq,
        file: UploadFile,
        session: AsyncSession,
        tmp_dir: Path,
    ) -> Document:
        """Create new document."""
        try:
            doc: Document = await doc_repo.create_doc(
                user_id=create_data.user_id,
                file_name=create_data.file_name,
                session=session,
            )
            try:
                # save temp file
                tmp_file = await file_handler.create_temp_file(
                    file=file,
                    file_dir=tmp_dir,
                )

            except Exception:
                await session.rollback()
                raise

            try:
                # load_document and split
                documents = await load_document(
                    file_path=str(tmp_file),
                )
                split_txt = await asyncio.to_thread(
                    split_document,
                    documents=documents,
                    doc_id=doc.id,
                    user_id=doc.user_id,
                    file_name=create_data.file_name,
                )

                # vectorize documents
                await vector_store.vectorize_documents(
                    collection_name=str(create_data.user_id),
                    documents=split_txt,
                )

            except Exception:
                await session.rollback()

                raise

            finally:
                await file_handler.delete_temp_file(tmp_file)

        except RepositoryException:
            await session.rollback()
            raise

        except Exception as exc:
            await session.rollback()
            raise ServiceException(
                (
                    "Service side error: Document creation failed."
                    f"\nDetails: '{exc!s}'."
                ),
            ) from exc

        await session.commit()

        return doc

    async def get_docs(
        self,
        user_id: UUID,
        session: AsyncSession,
    ) -> list[Document]:
        """Get user documents."""
        try:
            docs: list[Document] = await doc_repo.get_docs(
                user_id=user_id,
                session=session,
            )

        except RepositoryException:
            raise

        except Exception as exc:
            raise ServiceException(
                "Service side error: Documents retrival failed.",
            ) from exc

        return docs

    async def get_doc(
        self,
        user_id: UUID,
        document_id: UUID,
        session: AsyncSession,
    ) -> Document:
        """Get user document."""
        try:
            doc: Document | None = await doc_repo.get_doc(
                user_id=user_id,
                document_id=document_id,
                session=session,
            )

            if doc is None:
                raise ServiceException(
                    f"Document {document_id} not found.",
                )

        except RepositoryException:
            raise

        except Exception as exc:
            raise ServiceException(
                "Service side error: Document retrival failed.",
            ) from exc

        return doc


doc_service = DocService()
