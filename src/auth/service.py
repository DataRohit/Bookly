from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import User
from .schemas import UserCreateSchema
from .utils import generate_password_hash


class UserService:
    async def create_user(
        self, user_data: UserCreateSchema, session: AsyncSession
    ) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=generate_password_hash(user_data.password),
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def get_user_by_email(self, email: str, session: AsyncSession) -> User:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        return user

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return True if user else False

    async def update_user(
        self, user: User, user_data: dict, session: AsyncSession
    ) -> User:
        for field, value in user_data.items():
            setattr(user, field, value)

        await session.commit()
        await session.refresh(user)

        return user
