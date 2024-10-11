import json

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from pkg.db import get_session
from pkg.utils import get_current_user_uid

from .schemas import (
    BookCategoryCreateSchema,
    BookCategoryResponseSchema,
    BookGenreCreateSchema,
    BookGenreResponseSchema,
)
from .service import BookCategoryService, BookGenreService

book_category_router = APIRouter()
book_genre_router = APIRouter()

book_category_service = BookCategoryService()
book_genre_service = BookGenreService()


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

    if str(book_category.created_by) != user_uid:
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


@book_category_router.get("/get/name/{category}", status_code=status.HTTP_200_OK)
async def get_book_category_by_id(
    category: str, session: AsyncSession = Depends(get_session)
):
    book_category = await book_category_service.get_book_category_by_category(
        category, session
    )

    if not book_category:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book category not found"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book category found",
            "book_category": BookCategoryResponseSchema(
                **json.loads(book_category.model_dump_json())
            ).model_dump(),
        },
    )


@book_category_router.get("/get/uid/{category_uid}", status_code=status.HTTP_200_OK)
async def get_book_category_by_uid(
    category_uid: str, session: AsyncSession = Depends(get_session)
):
    book_category = await book_category_service.get_book_category_by_uid(
        category_uid, session
    )

    if not book_category:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book category not found"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book category found",
            "book_category": BookCategoryResponseSchema(
                **json.loads(book_category.model_dump_json())
            ).model_dump(),
        },
    )


@book_genre_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_book_genre(
    genre_data: BookGenreCreateSchema,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    book_genre = await book_genre_service.get_book_genre_by_genre(
        genre_data.genre, session
    )
    if book_genre:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Book genre already exists"},
        )

    book_genre = await book_genre_service.create_book_genre(
        user_uid, genre_data, session
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Book genre created successfully",
            "book_genre": BookGenreResponseSchema(
                **json.loads(book_genre.model_dump_json())
            ).model_dump(),
        },
    )


@book_genre_router.patch("/update/{genre_uid}", status_code=status.HTTP_200_OK)
async def update_book_genre(
    genre_uid: str,
    genre_data: BookGenreCreateSchema,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    book_genre = await book_genre_service.get_book_genre_by_uid(genre_uid, session)

    if not book_genre:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book genre not found"},
        )

    if str(book_genre.created_by) != user_uid:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "You are not allowed to update this book genre"},
        )

    book_genre = await book_genre_service.update_book_genre(
        book_genre, genre_data.model_dump(), session
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book genre updated successfully",
            "book_genre": BookGenreResponseSchema(
                **json.loads(book_genre.model_dump_json())
            ).model_dump(),
        },
    )


@book_genre_router.get("/list", status_code=status.HTTP_200_OK)
async def list_book_genres(session: AsyncSession = Depends(get_session)):
    book_genres = await book_genre_service.list_book_genres(session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "List of book genres",
            "book_genres": [
                BookGenreResponseSchema(
                    **json.loads(book_genre.model_dump_json())
                ).model_dump()
                for book_genre in book_genres
            ],
        },
    )


@book_genre_router.get("/get/name/{genre}", status_code=status.HTTP_200_OK)
async def get_book_genre_by_id(
    genre: str, session: AsyncSession = Depends(get_session)
):
    book_genre = await book_genre_service.get_book_genre_by_genre(genre, session)

    if not book_genre:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book genre not found"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book genre found",
            "book_genre": BookGenreResponseSchema(
                **json.loads(book_genre.model_dump_json())
            ).model_dump(),
        },
    )


@book_genre_router.get("/get/uid/{genre_uid}", status_code=status.HTTP_200_OK)
async def get_book_genre_by_uid(
    genre_uid: str, session: AsyncSession = Depends(get_session)
):
    book_genre = await book_genre_service.get_book_genre_by_uid(genre_uid, session)

    if not book_genre:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book genre not found"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book genre found",
            "book_genre": BookGenreResponseSchema(
                **json.loads(book_genre.model_dump_json())
            ).model_dump(),
        },
    )
