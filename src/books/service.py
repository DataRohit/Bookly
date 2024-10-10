from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import BookCategory, BookGenre


class BookCategoryService:
    async def create_book_category(
        self, user_uid: str, category_data: dict, session: AsyncSession
    ):
        book_category = BookCategory(
            category=category_data.category,
            description=category_data.description,
            created_by=user_uid,
        )
        session.add(book_category)
        await session.commit()
        await session.refresh(book_category)

        return book_category

    async def update_book_category(
        self, book_category: BookCategory, category_data: dict, session: AsyncSession
    ):
        for field, value in category_data.items():
            setattr(book_category, field, value)

        await session.commit()
        await session.refresh(book_category)

        return book_category

    async def get_book_category_by_uid(self, uid: str, session: AsyncSession):
        result = await session.execute(
            select(BookCategory).where(BookCategory.uid == uid)
        )
        book_category = result.scalars().first()
        return book_category

    async def get_book_category_by_category(self, category: str, session: AsyncSession):
        result = await session.execute(
            select(BookCategory).where(BookCategory.category == category)
        )
        book_category = result.scalars().first()
        return book_category

    async def list_book_categories(self, session: AsyncSession):
        result = await session.execute(select(BookCategory))
        book_categories = result.scalars().all()
        return book_categories


class BookGenreService:
    async def create_book_genre(
        self, user_uid: str, genre_data: dict, session: AsyncSession
    ):
        book_genre = BookGenre(
            genre=genre_data.genre,
            description=genre_data.description,
            created_by=user_uid,
        )
        session.add(book_genre)
        await session.commit()
        await session.refresh(book_genre)

        return book_genre

    async def update_book_genre(
        self, book_genre: BookGenre, genre_data: dict, session: AsyncSession
    ):
        for field, value in genre_data.items():
            setattr(book_genre, field, value)

        await session.commit()
        await session.refresh(book_genre)

        return book_genre

    async def get_book_genre_by_uid(self, uid: str, session: AsyncSession):
        result = await session.execute(select(BookGenre).where(BookGenre.uid == uid))
        book_genre = result.scalars().first()
        return book_genre

    async def get_book_genre_by_genre(self, genre: str, session: AsyncSession):
        result = await session.execute(
            select(BookGenre).where(BookGenre.genre == genre)
        )
        book_genre = result.scalars().first()
        return book_genre

    async def list_book_genres(self, session: AsyncSession):
        result = await session.execute(select(BookGenre))
        book_genres = result.scalars().all()
        return book_genres
