import json

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from pkg.db import get_session
from pkg.utils import get_current_user_uid
from src.auth.service import UserService

from .schemas import UserProfileResponseSchema, UserProfileUpdateSchema
from .service import UserProfileService

profile_router = APIRouter()

user_service = UserService()
user_profile_service = UserProfileService()


@profile_router.put("/", status_code=status.HTTP_200_OK)
async def update_user_profile(
    profile_data: UserProfileUpdateSchema,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    user_profile = await user_profile_service.get_user_profile_by_user_uid(
        user_uid, session
    )
    user_profile = await user_profile_service.update_user_profile(
        user_profile, profile_data.model_dump(), session
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User profile updated successfully",
            "user_profile": UserProfileResponseSchema(
                **json.loads(user_profile.model_dump_json())
            ).model_dump(),
        },
    )
