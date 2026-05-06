"""Mixin schemes."""

from datetime import (
    datetime,
)
from uuid import uuid4

from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
)


class IdUUIDMixin(BaseModel):
    """ID UUID mixin."""

    id: UUID4 = Field(
        default_factory=uuid4,
    )


class ResponseMixin(BaseModel):
    """Response mixin."""

    model_config = ConfigDict(from_attributes=True)


class CreatedAtMixin(BaseModel):
    """Created at mixin."""

    created_at: datetime


class BaseResponseMixin(ResponseMixin, IdUUIDMixin, CreatedAtMixin):
    """Base response mixin."""
