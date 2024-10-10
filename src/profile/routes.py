import json
import os

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from pkg.config import Config
from pkg.db import get_session
from pkg.utils import get_current_user_uid
from src.auth.service import UserService

from .schemas import UserProfileResponseSchema, UserProfileUpdateSchema
from .service import UserProfileService
from .tasks import upload_user_avatar_image_task

profile_router = APIRouter()

user_service = UserService()
user_profile_service = UserProfileService()


@profile_router.patch("/update-profile", status_code=status.HTTP_200_OK)
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


@profile_router.patch("/update-avatar", status_code=status.HTTP_200_OK)
async def update_user_avatar(
    request: Request,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    user_profile = await user_profile_service.get_user_profile_by_user_uid(
        user_uid, session
    )

    form = await request.form()
    avatar_image = form.get("avatar_image")

    if not avatar_image:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Avatar image is required"},
        )

    avatar_image_content = await avatar_image.read()
    avatar_image_file_extension = os.path.splitext(avatar_image.filename)[1]
    avatar_image_file_name = f"avatars/{user_uid}{avatar_image_file_extension}"

    upload_user_avatar_image_task.delay(
        avatar_image_content,
        avatar_image_file_name,
        avatar_image.content_type,
    )

    file_url = f"http://{Config.MINIO_STORAGE_ENDPOINT}/{Config.MINIO_STORAGE_BUCKET}/{avatar_image_file_name}"
    await user_profile_service.update_user_profile_avatar(
        user_profile, file_url, session
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User avatar updated successfully",
            "user_profile": UserProfileResponseSchema(
                **json.loads(user_profile.model_dump_json())
            ).model_dump(),
        },
    )
