from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import BookCategory


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
