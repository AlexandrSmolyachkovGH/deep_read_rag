"""User models file."""

from typing import TYPE_CHECKING

from sqlalchemy import (
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
    from app.models.documents import Document


class User(Base, UUIDPkMixin, CreatedAtMixin):
    """User model."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )
    documents: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="user",
        passive_deletes=True,
    )

    def __str__(self) -> str:
        """Model string representation."""
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"email={self.email}, "
            f"created_at={self.created_at})"
        )

    def __repr__(self) -> str:
        """Represented value of the model."""
        return str(self)
