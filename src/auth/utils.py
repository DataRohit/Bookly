import bcrypt

from pkg.config import Config


def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt(rounds=Config.BCRYPT_ROUND)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def veryfy_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
