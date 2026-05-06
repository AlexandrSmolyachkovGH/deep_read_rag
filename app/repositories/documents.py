"""Document's repository."""

from uuid import UUID

from sqlalchemy import (
    select,
)
from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.custom_exceptions import RepositoryException
from app.models.documents import (
    Document,
)


class DocumentRepo:
    """Document's repository."""

    async def create_doc(
        self,
        user_id: UUID,
        file_name: str,
        session: AsyncSession,
    ) -> Document:
        """Create new document."""
        try:
            new_doc = Document(
                user_id=user_id,
                file_name=file_name,
            )
            session.add(new_doc)
            await session.flush()

        except (SQLAlchemyError, IntegrityError) as exc:
            raise RepositoryException(
                "DB side error: Document creation failed.",
            ) from exc

        return new_doc

    async def get_doc(
        self,
        user_id: UUID,
        document_id: UUID,
        session: AsyncSession,
    ) -> Document | None:
        """Get user document."""
        try:
            stmt = select(Document).where(
                Document.user_id == user_id,
                Document.id == document_id,
            )
            scalar_res = await session.execute(stmt)

            doc: Document | None = scalar_res.scalar_one_or_none()

        except (SQLAlchemyError, IntegrityError) as exc:
            raise RepositoryException(
                "DB side error: Document retrival failed.",
            ) from exc

        return doc

    async def get_docs(
        self,
        user_id: UUID,
        session: AsyncSession,
    ) -> list[Document]:
        """Get user's documents."""
        try:
            stmt = select(Document).where(
                Document.user_id == user_id,
            )
            scalar_res = await session.execute(stmt)

            docs = scalar_res.scalars()

        except (SQLAlchemyError, IntegrityError) as exc:
            raise RepositoryException(
                "DB side error: Documents retrival failed.",
            ) from exc

        return list(docs)


doc_repo = DocumentRepo()
