import bcrypt
from itsdangerous import URLSafeTimedSerializer

from pkg.config import Config

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
