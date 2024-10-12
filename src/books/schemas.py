from pydantic import BaseModel, Field


class BookCategoryCreateSchema(BaseModel):
    category: str = Field(
        max_length=50,
        description="The name of the book category. This field must be unique.",
    )
    description: str = Field(
        max_length=500, description="A brief description of the book category."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "category": "Science Fiction",
                "description": "Books that explore the future of humanity, technology, and the universe.",
            }
        }
    }


class BookCategoryResponseSchema(BaseModel):
    uid: str
    category: str
    description: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "category": "Science Fiction",
                "description": "Books that explore the future of humanity, technology, and the universe.",
            }
        }
    }


class BookGenreCreateSchema(BaseModel):
    genre: str = Field(
        max_length=50,
        description="The name of the book genre. This field must be unique.",
    )
    description: str = Field(
        max_length=500, description="A brief description of the book genre."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "genre": "Fantasy",
                "description": "Books that feature magic, mythical creatures, and epic adventures.",
            }
        }
    }


class BookGenreResponseSchema(BaseModel):
    uid: str
    genre: str
    description: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "genre": "Fantasy",
                "description": "Books that feature magic, mythical creatures, and epic adventures.",
            }
        }
    }


class BookCreateSchema(BaseModel):
    title: str = Field(
        max_length=100, description="The title of the book. This field must be unique."
    )
    description: str = Field(
        max_length=500, description="A brief description of the book."
    )
    isbn: str = Field(
        max_length=20,
        description="The International Standard Book Number (ISBN) of the book. This field must be unique.",
    )
    published_date: str = Field(
        description="The date when the book was published. The date must be in the format YYYY-MM-DD."
    )
    page_count: int = Field(ge=1, description="The number of pages in the book.")
    authors: list[str] = Field(description="A list of the authors' full names.")
    categories: list[str] = Field(description="A list of the book categories.")
    genres: list[str] = Field(description="A list of the book genres.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Dune",
                "description": "A science fiction novel about the desert planet Arrakis.",
                "isbn": "9780441172719",
                "published_date": "1965-06-01",
                "page_count": 604,
                "authors": ["Frank Herbert"],
                "categories": ["Fiction"],
                "genres": ["Science Fiction"],
            }
        }
    }


class BookResponseSchema(BaseModel):
    uid: str
    title: str
    description: str
    isbn: str
    published_date: str
    page_count: int
    authors: list[str]
    categories: list[str]
    genres: list[str]
    images: list[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Dune",
                "description": "A science fiction novel about the desert planet Arrakis.",
                "isbn": "9780441172719",
                "published_date": "1965-06-01",
                "page_count": 604,
                "authors": ["Frank Herbert"],
                "categories": ["Fiction"],
                "genres": ["Science Fiction"],
                "images": [
                    "https://example.com/book-image-1.jpg",
                    "https://example.com/book-image-2.jpg",
                    "https://example.com/book-image-3.jpg",
                ],
            }
        }
    }
