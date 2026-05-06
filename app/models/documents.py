"""Document models file."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as UUID_A,
)
from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import Base
from app.models.mixins.mixins import (
    CreatedAtMixin,
    UUIDPkMixin,
)

if TYPE_CHECKING:
    from app.models.users import User


class Document(Base, UUIDPkMixin, CreatedAtMixin):
    """Document model."""

    __tablename__ = "documents"

    user_id: Mapped[UUID] = mapped_column(
        UUID_A(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    file_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="documents",
    )

    def __str__(self) -> str:
        """Model string representation."""
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"file_name={self.file_name}, "
            f"created_at={self.created_at})"
        )

    def __repr__(self) -> str:
        """Represented value of the model."""
        return str(self)
