from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")

    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    BCRYPT_ROUND: int = Field(..., env="BCRYPT_ROUND")

    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field(..., env="JWT_ALGORITHM")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
