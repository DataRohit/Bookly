import json
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from pkg.config import Config
from pkg.db import get_session
from pkg.errors import UserAlreadyExists
from pkg.mail import send_email

from .schemas import (
    UserCreateResponseSchema,
    UserCreateSchema,
    UserForgotPasswordSchema,
)
from .service import UserService
from .utils import decode_url_safe_token, generate_url_safe_token

auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    if await user_service.user_exists(user_data.email, session):
        raise UserAlreadyExists

    user = await user_service.create_user(user_data, session)

    user_activation_token = generate_url_safe_token(
        {
            "user_uid": str(user.uid),
            "expires_at": (datetime.now() + timedelta(minutes=15)).timestamp(),
        }
    )
    user_activation_link = (
        f"http://{Config.DOMAIN}/api/v1/auth/activate/{user_activation_token}"
    )

    await send_email(
        [user.email],
        "Activate your account",
        "auth/activation_email.html",
        {"first_name": user.first_name, "activation_link": user_activation_link},
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User registered successfully",
            "user": UserCreateResponseSchema(
                **json.loads(user.model_dump_json())
            ).model_dump(),
        },
    )


@auth_router.post("/activate/{activation_token}", status_code=status.HTTP_200_OK)
async def activate_user(
    activation_token: str,
    session: AsyncSession = Depends(get_session),
):
    data = decode_url_safe_token(activation_token)

    user_uid = data.get("user_uid")
    expires_at = data.get("expires_at")

    if not user_uid or not expires_at:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid activation token"},
        )

    if datetime.now().timestamp() > expires_at:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Activation token expired"},
        )

    user = await user_service.get_user_by_uid(user_uid, session)
    if user.is_verified or user.is_active:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "User already activated"},
        )

    await user_service.activate_user(user_uid, session)

    await send_email(
        [user.email],
        "Acount Activated Successfully",
        "auth/activation_success_email.html",
        {"first_name": user.first_name},
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User activated successfully",
            "user": UserCreateResponseSchema(
                **json.loads(user.model_dump_json())
            ).model_dump(),
        },
    )


@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    user_data: UserForgotPasswordSchema,
    session: AsyncSession = Depends(get_session),
):
    user = await user_service.get_user_by_email(user_data.email, session)

    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"},
        )

    password_reset_token = generate_url_safe_token(
        {
            "user_uid": str(user.uid),
            "expires_at": (datetime.now() + timedelta(minutes=15)).timestamp(),
        }
    )
    password_reset_link = (
        f"http://{Config.DOMAIN}/api/v1/auth/reset-password/{password_reset_token}"
    )

    await send_email(
        [user.email],
        "Reset your password",
        "auth/forgot_password_email.html",
        {"first_name": user.first_name, "password_reset_link": password_reset_link},
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Password reset link sent to your email"},
    )
