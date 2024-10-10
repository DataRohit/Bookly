from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import UserProfile


class UserProfileService:
    async def update_user_profile(
        self, user_profile: UserProfile, profile_data: dict, session: AsyncSession
    ) -> UserProfile:
        for field, value in profile_data.items():
            setattr(user_profile, field, value)

        await session.commit()
        await session.refresh(user_profile)

        return user_profile

    async def get_user_profile_by_user_uid(
        self, user_uid: str, session: AsyncSession
    ) -> UserProfile:
        result = await session.execute(
            select(UserProfile).where(UserProfile.user_uid == user_uid)
        )
        user_profile = result.scalars().first()
        return user_profile
