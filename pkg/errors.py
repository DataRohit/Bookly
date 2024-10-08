from typing import Any, Callable

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class BooklyException(Exception):
    pass


class InvalidToken(BooklyException):
    pass


class RevokedToken(BooklyException):
    pass


class AccessTokenRequired(BooklyException):
    pass


class RefreshTokenRequired(BooklyException):
    pass


class UserAlreadyExists(BooklyException):
    pass


class InvalidCredentials(BooklyException):
    pass


class InsufficientPermission(BooklyException):
    pass


class BookNotFound(BooklyException):
    pass


class TagNotFound(BooklyException):
    pass


class TagAlreadyExists(BooklyException):
    pass


class UserNotFound(BooklyException):
    pass


class AccountNotVerified(BooklyException):
    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BooklyException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    error_configs = [
        (
            UserAlreadyExists,
            status.HTTP_403_FORBIDDEN,
            {"message": "User with email already exists", "error_code": "user_exists"},
        ),
        (
            UserNotFound,
            status.HTTP_404_NOT_FOUND,
            {"message": "User not found", "error_code": "user_not_found"},
        ),
        (
            BookNotFound,
            status.HTTP_404_NOT_FOUND,
            {"message": "Book not found", "error_code": "book_not_found"},
        ),
        (
            InvalidCredentials,
            status.HTTP_400_BAD_REQUEST,
            {
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
        (
            InvalidToken,
            status.HTTP_401_UNAUTHORIZED,
            {
                "message": "Token is invalid or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
        (
            RevokedToken,
            status.HTTP_401_UNAUTHORIZED,
            {
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
        (
            AccessTokenRequired,
            status.HTTP_401_UNAUTHORIZED,
            {
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
        (
            RefreshTokenRequired,
            status.HTTP_403_FORBIDDEN,
            {
                "message": "Please provide a valid refresh token",
                "resolution": "Please get a refresh token",
                "error_code": "refresh_token_required",
            },
        ),
        (
            InsufficientPermission,
            status.HTTP_401_UNAUTHORIZED,
            {
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
        (
            TagNotFound,
            status.HTTP_404_NOT_FOUND,
            {"message": "Tag Not Found", "error_code": "tag_not_found"},
        ),
        (
            TagAlreadyExists,
            status.HTTP_403_FORBIDDEN,
            {"message": "Tag already exists", "error_code": "tag_exists"},
        ),
        (
            AccountNotVerified,
            status.HTTP_403_FORBIDDEN,
            {
                "message": "Account not verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details",
            },
        ),
    ]

    for exc_class, status_code, detail in error_configs:
        app.add_exception_handler(
            exc_class,
            create_exception_handler(status_code=status_code, initial_detail=detail),
        )

    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            content={"message": "Database error occurred", "error_code": "db_error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
