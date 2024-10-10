from fastapi import FastAPI

from pkg.middleware import register_middleware
from src.auth.routes import auth_router
from src.books.routes import book_category_router, book_genre_router
from src.profile.routes import profile_router

version = "v1"

description = """
Bookly is an innovative online platform designed for book lovers to connect and share their personal collections. Users can easily list the novels and books they own, making them available for others to purchase or borrow. Whether you’re looking to clear space on your bookshelf, discover new reads, or lend a hand to fellow readers, Bookly creates a community-driven marketplace for exchanging books. With a simple and user-friendly interface, Bookly makes it effortless to explore a wide variety of titles, fostering a sustainable and connected book-sharing experience.

This REST API Can:
- User Authentication (Register, Login, Logout, User Activation, Reset Password, etc.)
"""

version_prefix = f"/api/{version}"

app = FastAPI(
    title="Bookly",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Rohit Vilas Ingole",
        "url": "https://github.com/dataorhit",
        "email": "rohit.vilas.ingole@gmail.com",
    },
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
)


register_middleware(app)


app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(profile_router, prefix=f"{version_prefix}/profile", tags=["profile"])
app.include_router(
    book_category_router,
    prefix=f"{version_prefix}/books/category",
    tags=["book_category"],
)
app.include_router(
    book_genre_router,
    prefix=f"{version_prefix}/books/genre",
    tags=["book_genre"],
)
