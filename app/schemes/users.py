"""User schemes."""

from pydantic import (
    BaseModel,
    EmailStr,
)

from app.schemes.mixins import (
    BaseResponseMixin,
)


class CreateUserReq(BaseModel):
    """Create user request scheme."""

    email: EmailStr


class CreateUserResp(BaseResponseMixin):
    """Create user response scheme."""

    email: EmailStr


class GetUserReq(BaseModel):
    """Get user request scheme."""

    email: EmailStr


class GetUserResp(BaseResponseMixin):
    """Get user request scheme."""

    email: EmailStr
