import json
import os

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from pkg.config import Config
from pkg.db import get_session
from pkg.tasks import upload_image_task
from pkg.utils import get_current_user_uid

from .schemas import (
    BookCategoryCreateSchema,
    BookCategoryResponseSchema,
    BookCreateSchema,
    BookGenreCreateSchema,
    BookGenreResponseSchema,
    BookResponseSchema,
)
from .service import BookCategoryService, BookGenreService, BookService

book_category_router = APIRouter()
book_genre_router = APIRouter()
book_router = APIRouter()

book_category_service = BookCategoryService()
book_genre_service = BookGenreService()
book_service = BookService()


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


@book_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreateSchema,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    book = await book_service.get_book_by_isbn(book_data.isbn, session)
    if book:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Book already exists"},
        )

    book = await book_service.get_book_by_title(book_data.title, session)
    if book:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Book already exists"},
        )

    book = await book_service.create_book(user_uid, book_data, session)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Book created successfully",
            "book": BookResponseSchema(
                **json.loads(book.model_dump_json())
            ).model_dump(),
        },
    )


@book_router.patch("/update/{book_uid}", status_code=status.HTTP_200_OK)
async def update_book(
    book_uid: str,
    book_data: BookCreateSchema,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    book = await book_service.get_book_by_uid(book_uid, session)

    if not book:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book not found"},
        )

    if str(book.created_by) != user_uid:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "You are not allowed to update this book"},
        )

    book = await book_service.update_book(book, book_data, session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book updated successfully",
            "book": BookResponseSchema(
                **json.loads(book.model_dump_json())
            ).model_dump(),
        },
    )


@book_router.get("/list", status_code=status.HTTP_200_OK)
async def list_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.list_books(session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "List of books",
            "books": [
                BookResponseSchema(**json.loads(book.model_dump_json())).model_dump()
                for book in books
            ],
        },
    )


@book_router.get("/get/isbn/{isbn}", status_code=status.HTTP_200_OK)
async def get_book_by_isbn(isbn: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book_by_isbn(isbn, session)

    if not book:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book not found"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book found",
            "book": BookResponseSchema(
                **json.loads(book.model_dump_json())
            ).model_dump(),
        },
    )


@book_router.get("/get/uid/{book_uid}", status_code=status.HTTP_200_OK)
async def get_book_by_uid(book_uid: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book_by_uid(book_uid, session)

    if not book:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book not found"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book found",
            "book": BookResponseSchema(
                **json.loads(book.model_dump_json())
            ).model_dump(),
        },
    )


@book_router.get("/get/title/{title}", status_code=status.HTTP_200_OK)
async def get_book_by_title(title: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book_by_title(title, session)

    if not book:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book not found"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book found",
            "book": BookResponseSchema(
                **json.loads(book.model_dump_json())
            ).model_dump(),
        },
    )


@book_router.get("/list/category/{category}", status_code=status.HTTP_200_OK)
async def list_books_by_category(
    category: str, session: AsyncSession = Depends(get_session)
):
    books = await book_service.list_books_by_category(category, session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "List of books by category",
            "books": [
                BookResponseSchema(**json.loads(book.model_dump_json())).model_dump()
                for book in books
            ],
        },
    )


@book_router.get("/list/genre/{genre}", status_code=status.HTTP_200_OK)
async def list_books_by_genre(genre: str, session: AsyncSession = Depends(get_session)):
    books = await book_service.list_books_by_genre(genre, session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "List of books by genre",
            "books": [
                BookResponseSchema(**json.loads(book.model_dump_json())).model_dump()
                for book in books
            ],
        },
    )


@book_router.get("/list/author/{author}", status_code=status.HTTP_200_OK)
async def list_books_by_author(
    author: str, session: AsyncSession = Depends(get_session)
):
    books = await book_service.list_books_by_author(author, session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "List of books by author",
            "books": [
                BookResponseSchema(**json.loads(book.model_dump_json())).model_dump()
                for book in books
            ],
        },
    )


@book_router.patch("/update/image/{book_uid}", status_code=status.HTTP_200_OK)
async def update_book_image(
    request: Request,
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    user_uid: str = Depends(get_current_user_uid),
):
    book = await book_service.get_book_by_uid(book_uid, session)

    if not book:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Book not found"},
        )

    form = await request.form()
    book_image = form.get("book_image")

    if not book_image:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Book image not found"},
        )

    if len(book.images) >= 5:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Book image limit reached"},
        )

    book_image_content = await book_image.read()
    book_image_extension = os.path.splitext(book_image.filename)[1]
    book_image_file_name = (
        f"book_images/{book_uid}-{len(book.images) + 1}{book_image_extension}"
    )

    upload_image_task.delay(
        book_image_content,
        book_image_file_name,
        book_image.content_type,
    )

    file_url = f"http://{Config.DOMAIN}/minio/storage/{Config.MINIO_STORAGE_BUCKET}/{book_image_file_name}"
    book = await book_service.update_book_image(book, file_url, session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Book image updated successfully",
            "book": BookResponseSchema(
                **json.loads(book.model_dump_json())
            ).model_dump(),
        },
    )
