from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")

    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    BCRYPT_ROUND: int = Field(..., env="BCRYPT_ROUND")

    MAIL_USER: str = Field(..., env="MAIL_USER")
    MAIL_PASSWORD: str = Field(..., env="MAIL_PASSWORD")
    MAIL_SERVER: str = Field(..., env="MAIL_SERVER")
    MAIL_PORT: int = Field(..., env="MAIL_PORT")
    MAIL_FROM: str = Field(..., env="MAIL_FROM")

    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_SALT: str = Field(..., env="JWT_SALT")
    JWT_ALGORITHM: str = Field(..., env="JWT_ALGORITHM")

    DOMAIN: str = Field(..., env="DOMAIN")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
