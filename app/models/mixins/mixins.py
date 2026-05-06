"""Model mixins."""

from datetime import datetime
from uuid import (
    UUID,
)

from sqlalchemy import (
    UUID as UUID_A,
)
from sqlalchemy import (
    DateTime,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class UUIDPkMixin:
    """ID UUID PK Mixin."""

    id: Mapped[UUID] = mapped_column(
        UUID_A(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )


class CreatedAtMixin:
    """Created_at Mixin."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
