from pydantic import BaseModel, Field


class UserProfileUpdateSchema(BaseModel):
    bio: str = Field(
        max_length=500,
        description="Tell the Bookly community a little about yourself! You can mention your favorite genres, what kinds of books you're currently reading or offering, and whether you're open to lending, borrowing, or selling books. Help others get to know your reading style and what you're looking for!",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "bio": "I love reading science fiction and fantasy novels. I'm currently reading the latest book in the Wheel of Time series and I'm open to lending and borrowing books.",
            }
        }
    }


class UserProfileResponseSchema(BaseModel):
    uid: str
    user_uid: str
    bio: str
    avatar: str
    created_at: str
    updated_at: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "user_uid": "123e4567-e89b-12d3-a456-426614174000",
                "bio": "I love reading science fiction and fantasy novels. I'm currently reading the latest book in the Wheel of Time series and I'm open to lending and borrowing books.",
                "avatar": "https://api.dicebear.com/9.x/adventurer-neutral/png?seed=Adrian",
                "created_at": "2024-10-08T09:22:21.361119",
                "updated_at": "2024-10-08T09:22:21.361119",
            }
        }
    }
