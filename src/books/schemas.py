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
