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
    UserResetPasswordSchema,
)
from .service import PasswordResetLogService, TokenBlackListService, UserService
from .utils import (
    decode_url_safe_token,
    generate_password_hash,
    generate_url_safe_token,
)

auth_router = APIRouter()

user_service = UserService()
token_blacklist_service = TokenBlackListService()
password_reset_log_service = PasswordResetLogService()


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
    token_blacklisted = await token_blacklist_service.check_token_blacklist(
        activation_token, session
    )
    if token_blacklisted:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Activation token blacklisted"},
        )

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

    await token_blacklist_service.blacklist_token(
        activation_token, datetime.fromtimestamp(expires_at), session
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
    forgot_password_request_exceeded = (
        await password_reset_log_service.check_password_reset_limit_exceeded(
            user_data.email, session
        )
    )
    if forgot_password_request_exceeded:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Password reset limit exceeded"},
        )

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

    await password_reset_log_service.log_password_reset(user.email, session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Password reset link sent to your email"},
    )


@auth_router.post(
    "/reset-password/{password_reset_token}", status_code=status.HTTP_200_OK
)
async def reset_password(
    password_reset_token: str,
    user_data: UserResetPasswordSchema,
    session: AsyncSession = Depends(get_session),
):
    token_blacklisted = await token_blacklist_service.check_token_blacklist(
        password_reset_token, session
    )
    if token_blacklisted:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Password reset token blacklisted"},
        )

    data = decode_url_safe_token(password_reset_token)

    user_uid = data.get("user_uid")
    expires_at = data.get("expires_at")

    if not user_uid or not expires_at:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid password reset token"},
        )

    if datetime.now().timestamp() > expires_at:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Password reset token expired"},
        )

    user = await user_service.get_user_by_uid(user_uid, session)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"},
        )

    if user_data.password != user_data.confirm_password:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Passwords do not match"},
        )

    user.hashed_password = generate_password_hash(user_data.password)

    await session.commit()
    await session.refresh(user)

    await send_email(
        [user.email],
        "Password Reset Successfully",
        "auth/reset_password_success_email.html",
        {"first_name": user.first_name},
    )

    await token_blacklist_service.blacklist_token(
        password_reset_token, datetime.fromtimestamp(expires_at), session
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Password reset successfully"},
    )
