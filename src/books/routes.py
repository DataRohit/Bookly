import json

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from pkg.db import get_session
from pkg.utils import get_current_user_uid

from .schemas import BookCategoryCreateSchema, BookCategoryResponseSchema
from .service import BookCategoryService

book_category_router = APIRouter()

book_category_service = BookCategoryService()


@book_category_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_book_category(
    category_data: BookCategoryCreateSchema,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    book_category = await book_category_service.get_book_category_by_category(
        category_data.category, session
    )
    if book_category:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Book category already exists"},
        )

    book_category = await book_category_service.create_book_category(
        user_uid, category_data, session
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Book category created successfully",
            "book_category": BookCategoryResponseSchema(
                **json.loads(book_category.model_dump_json())
            ).model_dump(),
        },
    )


@book_category_router.patch("/update/{category_uid}", status_code=status.HTTP_200_OK)
async def update_book_category(
    category_uid: str,
    category_data: BookCategoryCreateSchema,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    book_category = await book_category_service.get_book_category_by_uid(
        category_uid, session
    )

    if not book_category:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book category not found"},
        )

    if book_category.created_by != user_uid:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "You are not allowed to update this book category"},
        )

    book_category = await book_category_service.update_book_category(
        book_category, category_data.model_dump(), session
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book category updated successfully",
            "book_category": BookCategoryResponseSchema(
                **json.loads(book_category.model_dump_json())
            ).model_dump(),
        },
    )


@book_category_router.get("/list", status_code=status.HTTP_200_OK)
async def list_book_categories(session: AsyncSession = Depends(get_session)):
    book_categories = await book_category_service.list_book_categories(session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "List of book categories",
            "book_categories": [
                BookCategoryResponseSchema(
                    **json.loads(book_category.model_dump_json())
                ).model_dump()
                for book_category in book_categories
            ],
        },
    )
