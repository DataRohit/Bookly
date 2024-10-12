from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Book, BookCategory, BookGenre


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

    async def list_book_categories(self, page: int, session: AsyncSession):
        result = await session.execute(
            select(BookCategory).offset((page - 1) * 10).limit(10)
        )
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

    async def list_book_genres(self, page: int, session: AsyncSession):
        result = await session.execute(
            select(BookGenre).offset((page - 1) * 10).limit(10)
        )
        book_genres = result.scalars().all()
        return book_genres


class BookService:
    async def create_book(self, user_uid: str, book_data: dict, session: AsyncSession):
        book = Book(
            title=book_data.title,
            description=book_data.description,
            isbn=book_data.isbn,
            published_date=book_data.published_date,
            page_count=book_data.page_count,
            authors=book_data.authors,
            categories=book_data.categories,
            genres=book_data.genres,
        )
        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    async def update_book(self, book: Book, book_data: dict, session: AsyncSession):
        for field, value in book_data.items():
            setattr(book, field, value)

        await session.commit()
        await session.refresh(book)

        return book

    async def get_book_by_uid(self, uid: str, session: AsyncSession):
        result = await session.execute(select(Book).where(Book.uid == uid))
        book = result.scalars().first()
        return book

    async def get_book_by_isbn(self, isbn: str, session: AsyncSession):
        result = await session.execute(select(Book).where(Book.isbn == isbn))
        book = result.scalars().first()
        return book

    async def get_book_by_title(self, title: str, session: AsyncSession):
        result = await session.execute(select(Book).where(Book.title == title))
        book = result.scalars().first()
        return book

    async def list_books(self, page: int, session: AsyncSession):
        result = await session.execute(select(Book).offset((page - 1) * 10).limit(10))
        books = result.scalars().all()
        return books

    async def list_books_by_category(
        self, category: str, page: int, session: AsyncSession
    ):
        result = await session.execute(
            select(Book).where(
                Book.categories.contains(category).offset((page - 1) * 10).limit(10)
            )
        )
        books = result.scalars().all()
        return books

    async def list_books_by_genre(self, genre: str, page: int, session: AsyncSession):
        result = await session.execute(
            select(Book)
            .where(Book.genres.contains(genre))
            .offset((page - 1) * 10)
            .limit(10)
        )
        books = result.scalars().all()
        return books

    async def list_books_by_author(self, author: str, page: int, session: AsyncSession):
        result = await session.execute(
            select(Book)
            .where(Book.authors.contains(author))
            .offset((page - 1) * 10)
            .limit(10)
        )
        books = result.scalars().all()
        return books

    async def update_book_image(
        self, book: Book, image_url: str, session: AsyncSession
    ):
        book.images.append(image_url)
        await session.commit()
        await session.refresh(book)
        return book
