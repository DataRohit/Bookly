from datetime import datetime, timedelta

from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import PasswordResetLog, TokenBlacklist, User
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

    async def get_user_by_uid(self, user_uid: str, session: AsyncSession) -> User:
        user = await session.get(User, user_uid)
        return user

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return True if user else False

    async def activate_user(self, user_uid: str, session: AsyncSession) -> None:
        user = await session.get(User, user_uid)
        user.is_verified = True
        user.is_active = True

        await session.commit()
        await session.refresh(user)

    async def update_user(
        self, user: User, user_data: dict, session: AsyncSession
    ) -> User:
        for field, value in user_data.items():
            setattr(user, field, value)

        await session.commit()
        await session.refresh(user)

        return user


class TokenBlackListService:
    async def blacklist_token(
        self, token: str, expires_at: datetime, session: AsyncSession
    ) -> None:
        token_blacklist = TokenBlacklist(token=token, expires_at=expires_at)
        session.add(token_blacklist)
        await session.commit()

    async def check_token_blacklist(self, token: str, session: AsyncSession) -> bool:
        result = await session.execute(
            select(TokenBlacklist).where(TokenBlacklist.token == token)
        )
        token = result.scalars().first()
        return True if token else False

    async def clear_expired_blacklisted_tokens(self, session: AsyncSession) -> None:
        stmt = delete(TokenBlacklist).where(TokenBlacklist.expires_at < datetime.now())
        await session.execute(stmt)
        await session.commit()


class PasswordResetLogService:
    async def log_password_reset(self, user_email: str, session: AsyncSession):
        log = PasswordResetLog(user_email=user_email)
        session.add(log)
        await session.commit()

    async def check_password_reset_limit_exceeded(
        self, user_email: str, session: AsyncSession
    ) -> bool:
        result = await session.execute(
            select(PasswordResetLog).where(
                PasswordResetLog.user_email == user_email,
                PasswordResetLog.requested_at >= (datetime.now() - timedelta(days=15)),
            )
        )
        logs = result.scalars().all()
        return len(logs) >= 5

    async def clear_password_reset_logs(self, session: AsyncSession) -> None:
        stmt = delete(PasswordResetLog).where(
            PasswordResetLog.requested_at < (datetime.now() - timedelta(days=15))
        )
        await session.execute(stmt)
        await session.commit()
