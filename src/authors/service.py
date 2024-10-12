from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Author


class AuthorService:
    async def create_author(self, author_data: dict, session: AsyncSession):
        pen_name = author_data.get("pen_name", None)

        if pen_name:
            profile_image = (
                f"https://api.dicebear.com/9.x/adventurer-neutral/png?seed={pen_name}"
            )
        else:
            profile_image = f"https://api.dicebear.com/9.x/adventurer-neutral/png?seed={author_data['first_name']}{author_data['last_name']}"

        author = Author(
            first_name=author_data["first_name"],
            last_name=author_data["last_name"],
            pen_name=pen_name,
            nationality=author_data["nationality"],
            biography=author_data["biography"],
            profile_image=profile_image,
        )

        session.add(author)
        await session.commit()
        await session.refresh(author)

        return author

    async def update_author(
        self, author: Author, author_data: dict, session: AsyncSession
    ):
        for field, value in author_data.items():
            setattr(author, field, value)

        await session.commit()
        await session.refresh(author)

        return author

    async def update_author_profile_image(
        self, author: Author, profile_image: str, session: AsyncSession
    ):
        author.profile_image = profile_image

        await session.commit()
        await session.refresh(author)

        return author

    async def get_author_by_uid(self, uid: str, session: AsyncSession):
        result = await session.execute(select(Author).where(Author.uid == uid))
        author = result.scalars().first()
        return author

    async def get_author_by_pen_name(self, pen_name: str, session: AsyncSession):
        result = await session.execute(
            select(Author).where(Author.pen_name == pen_name)
        )
        author = result.scalars().first()
        return author

    async def get_author_by_name(
        self, first_name: str, last_name: str, session: AsyncSession
    ):
        result = await session.execute(
            select(Author)
            .where(Author.first_name == first_name)
            .where(Author.last_name == last_name)
        )
        author = result.scalars().first()
        return author

    async def list_authors_by_nationality(
        self, nationality: str, page: int, session: AsyncSession
    ):
        result = await session.execute(
            select(Author)
            .where(Author.nationality == nationality)
            .offset((page - 1) * 10)
            .limit(10)
        )
        authors = result.scalars().all()
        return authors

    async def list_authors(self, page: int, session: AsyncSession):
        result = await session.execute(select(Author).offset((page - 1) * 10).limit(10))
        authors = result.scalars().all()
        return authors
