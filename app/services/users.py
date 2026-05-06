"""User's service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.custom_exceptions import (
    RepositoryException,
    ServiceException,
)
from app.models.users import User
from app.repositories.user_repo import user_repo
from app.schemes.users import (
    CreateUserReq,
    GetUserReq,
)


class UserService:
    """User's service."""

    async def get_user(
        self,
        get_user_data: GetUserReq,
        session: AsyncSession,
    ) -> User:
        """Get user by email."""
        try:
            user: User | None = await user_repo.get_user_by_email(
                email=get_user_data.email,
                session=session,
            )

            if not user:
                raise ServiceException(
                    f"User: {get_user_data.email} - wasn't found.",
                )

        except RepositoryException as exc:
            raise ServiceException("Repository side error") from exc

        except Exception as exc:
            raise ServiceException(
                "Service side error: User retrival failed.",
            ) from exc

        return user

    async def create_user(
        self,
        create_data: CreateUserReq,
        session: AsyncSession,
    ) -> User:
        """Create new user."""
        try:
            user: User = await user_repo.create_user(
                email=create_data.email,
                session=session,
            )

            await session.commit()

        except RepositoryException as exc:
            raise ServiceException("Repository side error") from exc

        except Exception as exc:
            raise ServiceException(
                "Service side error: User creation failed.",
            ) from exc

        return user


user_service = UserService()
