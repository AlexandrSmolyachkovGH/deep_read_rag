"""User's repository."""

from sqlalchemy import select
from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.custom_exceptions import RepositoryException
from app.models.users import User


class UserRepo:
    """User's repository."""

    async def create_user(
        self,
        email: str,
        session: AsyncSession,
    ) -> User:
        """Create new user."""
        try:
            new_user = User(
                email=email,
            )
            session.add(new_user)
            await session.flush()

        except (SQLAlchemyError, IntegrityError) as exc:
            raise RepositoryException(
                "DB side error: User creation failed.",
            ) from exc

        return new_user

    async def get_user_by_email(
        self,
        email: str,
        session: AsyncSession,
    ) -> User | None:
        """Get user by email."""
        try:
            stmt = select(User).where(User.email == email)
            scalar_res = await session.execute(stmt)

            user: User | None = scalar_res.scalar_one_or_none()

        except (SQLAlchemyError, IntegrityError) as exc:
            raise RepositoryException(
                "DB side error: User retrival failed.",
            ) from exc

        return user


user_repo = UserRepo()
