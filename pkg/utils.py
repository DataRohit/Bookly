from datetime import datetime

import bcrypt
from fastapi import Cookie, HTTPException, status
from itsdangerous import URLSafeTimedSerializer

from .config import Config

url_safe_timed_serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, salt=Config.JWT_SALT
)


def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt(rounds=Config.BCRYPT_ROUND)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def generate_url_safe_token(data: dict) -> str:
    return url_safe_timed_serializer.dumps(data)


def decode_url_safe_token(token: str) -> dict:
    return url_safe_timed_serializer.loads(token)


def verify_url_safe_token(token: str) -> str:
    data = decode_url_safe_token(token)

    user_uid = data.get("user_uid")
    expires_at = data.get("expires_at")

    if not user_uid or not expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid access token",
        )

    if datetime.now().timestamp() > expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Access token expired",
        )

    return user_uid


def get_current_user_uid(access_token: str = Cookie(None)) -> str:
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required",
        )

    return verify_url_safe_token(access_token)
