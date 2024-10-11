from pydantic import BaseModel, Field


class AuthorCreateSchema(BaseModel):
    first_name: str = Field(max_length=50, description="The first name of the author.")
    last_name: str = Field(max_length=50, description="The last name of the author.")
    pen_name: str = Field(
        max_length=50,
        description="The pen name of the author, if they have one.",
    )
    nationality: str = Field(
        max_length=50, description="The country to which the author belongs."
    )
    biography: str = Field(description="A brief biography of the author.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "Isaac",
                "last_name": "Asimov",
                "pen_name": "Paul French",
                "nationality": "Russian",
                "biography": "Isaac Asimov was a Russian-born American author, professor, and biochemist, best known for his works of science fiction and popular science.",
            }
        }
    }


class AuthorResponseSchema(BaseModel):
    uid: str
    first_name: str
    last_name: str
    pen_name: str
    nationality: str
    biography: str
    profile_image: str
    created_at: str
    updated_at: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "first_name": "Isaac",
                "last_name": "Asimov",
                "pen_name": "Paul French",
                "nationality": "Russian",
                "biography": "Isaac Asimov was a Russian-born American author, professor, and biochemist, best known for his works of science fiction and popular science.",
                "profile_image": "https://example.com/profile-image.jpg",
                "created_at": "2021-07-01T12:00:00",
                "updated_at": "2021-07-01T12:00:00",
            }
        }
    }
