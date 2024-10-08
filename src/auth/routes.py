import json

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from pkg.db import get_session
from pkg.errors import UserAlreadyExists

from .schemas import UserCreateResponseSchema, UserCreateSchema
from .service import UserService

auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreateSchema,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    if await user_service.user_exists(user_data.email, session):
        raise UserAlreadyExists

    user = await user_service.create_user(user_data, session)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User registered successfully",
            "user": UserCreateResponseSchema(
                **json.loads(user.model_dump_json())
            ).model_dump(),
        },
    )
