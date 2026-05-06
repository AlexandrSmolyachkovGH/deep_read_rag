"""Document schemes."""

from pydantic import (
    UUID4,
    BaseModel,
)

from app.schemes.mixins import BaseResponseMixin


class CreateDocReq(BaseModel):
    """Create doc request scheme."""

    user_id: UUID4
    file_name: str


class CreateDocResp(BaseResponseMixin):
    """Create doc response scheme."""

    user_id: UUID4
    file_name: str


class GetDocReq(BaseModel):
    """Get doc request scheme."""

    user_id: UUID4
    file_name: str


class GetDocResp(BaseResponseMixin):
    """Get user request scheme."""

    user_id: UUID4
    file_name: str
