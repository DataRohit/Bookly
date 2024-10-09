from pydantic import BaseModel, Field


class UserCreateSchema(BaseModel):
    username: str = Field(max_length=25)
    email: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "JohnDoe@Password123",
            }
        }
    }


class UserCreateResponseSchema(BaseModel):
    uid: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_verified: bool
    is_active: bool
    created_at: str
    updated_at: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "role": "user",
                "is_verified": False,
                "is_active": False,
                "created_at": "2024-10-08T09:22:21.361119",
                "updated_at": "2024-10-08T09:22:21.361119",
            }
        }
    }


class UserForgotPasswordSchema(BaseModel):
    email: str = Field(max_length=50)

    model_config = {"json_schema_extra": {"example": {"email": "johndoe@example.com"}}}


class UserResetPasswordSchema(BaseModel):
    password: str = Field(min_length=8, max_length=50)
    confirm_password: str = Field(min_length=8, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "password": "JohnDoe@Password123",
                "confirm_password": "JohnDoe@Password123",
            }
        }
    }


class UserLoginSchema(BaseModel):
    email: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "johndoe@example.com",
                "password": "JohnDoe@Password123",
            }
        }
    }
