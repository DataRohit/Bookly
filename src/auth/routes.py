import json
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from pkg.config import Config
from pkg.db import get_session
from pkg.errors import UserAlreadyExists
from pkg.mail import send_email

from .schemas import UserCreateResponseSchema, UserCreateSchema
from .service import UserService
from .utils import generate_url_safe_token

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
        f"http://{Config.DOMAIN}/auth/activate/{user_activation_token}"
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
