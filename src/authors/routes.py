import json
import os

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from pkg.config import Config
from pkg.db import get_session
from pkg.tasks import upload_image_task
from pkg.utils import get_current_user_uid

from .schemas import AuthorCreateSchema, AuthorResponseSchema
from .service import AuthorService

author_router = APIRouter()

author_service = AuthorService()


@author_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_author(
    author_data: AuthorCreateSchema,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    author = await author_service.get_author_by_name(
        author_data.first_name, author_data.last_name, session
    )
    if author:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Author already exists"},
        )

    author = await author_service.get_author_by_pen_name(author_data.pen_name, session)
    if author:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Author already exists"},
        )

    author = await author_service.create_author(author_data.model_dump(), session)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Author created successfully",
            "author": AuthorResponseSchema(
                **json.loads(author.model_dump_json())
            ).model_dump(),
        },
    )


@author_router.patch("/update/{author_uid}", status_code=status.HTTP_200_OK)
async def update_author(
    author_uid: str,
    author_data: AuthorCreateSchema,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    author = await author_service.get_author_by_uid(author_uid, session)
    if not author:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Author not found"},
        )

    author = await author_service.update_author(
        author, author_data.model_dump(), session
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Author updated successfully",
            "author": AuthorResponseSchema(
                **json.loads(author.model_dump_json())
            ).model_dump(),
        },
    )


@author_router.patch(
    "/update/profile_image/{author_uid}", status_code=status.HTTP_200_OK
)
async def update_author_profile_image(
    author_uid: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    author = await author_service.get_author_by_uid(author_uid, session)
    if not author:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Author not found"},
        )

    form = await request.form()
    profile_image = form.get("profile_image")

    if not profile_image:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Profile image is required"},
        )

    profile_image_content = await profile_image.read()
    profile_image_file_extension = os.path.splitext(profile_image.filename)[1]
    profile_image_file_name = (
        f"author_profile_images/{author_uid}{profile_image_file_extension}"
    )

    upload_image_task.delay(
        profile_image_content,
        profile_image_file_name,
        profile_image.content_type,
    )

    file_url = f"http://{Config.DOMAIN}/minio/storage/{Config.MINIO_STORAGE_BUCKET}/{profile_image_file_name}"
    await author_service.update_author_profile_image(author, file_url, session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Author profile image updated successfully",
            "author": AuthorResponseSchema(
                **json.loads(author.model_dump_json())
            ).model_dump(),
        },
    )


@author_router.get("/list", status_code=status.HTTP_200_OK)
async def list_authors(session: AsyncSession = Depends(get_session)):
    authors = await author_service.list_authors(session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Authors retrieved successfully",
            "authors": [
                AuthorResponseSchema(
                    **json.loads(author.model_dump_json())
                ).model_dump()
                for author in authors
            ],
        },
    )


@author_router.get("/list/{nationality}", status_code=status.HTTP_200_OK)
async def list_authors_by_nationality(
    nationality: str, session: AsyncSession = Depends(get_session)
):
    authors = await author_service.list_authors_by_nationality(nationality, session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Authors retrieved successfully",
            "authors": [
                AuthorResponseSchema(
                    **json.loads(author.model_dump_json())
                ).model_dump()
                for author in authors
            ],
        },
    )


@author_router.get("/get/pen_name/{pen_name}", status_code=status.HTTP_200_OK)
async def get_author_by_pen_name(
    pen_name: str, session: AsyncSession = Depends(get_session)
):
    author = await author_service.get_author_by_pen_name(pen_name, session)

    if not author:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Author not found"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Author found",
            "author": AuthorResponseSchema(
                **json.loads(author.model_dump_json())
            ).model_dump(),
        },
    )


@author_router.get("/get/uid/{author_uid}", status_code=status.HTTP_200_OK)
async def get_author_by_uid(
    author_uid: str, session: AsyncSession = Depends(get_session)
):
    author = await author_service.get_author_by_uid(author_uid, session)

    if not author:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Author not found"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Author found",
            "author": AuthorResponseSchema(
                **json.loads(author.model_dump_json())
            ).model_dump(),
        },
    )
