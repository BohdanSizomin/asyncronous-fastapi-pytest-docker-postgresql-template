from functools import lru_cache
from typing import Literal

from pydantic import EmailStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: Literal["DEV", "TEST", "PROD"] = "DEV"
    JWT_SECRET: str = "default_secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    # DB
    DATABASE_NAME: str = "db"
    DATABASE_USERNAME: str = "postgres"
    DATABASE_PASSWORD: str = "password"
    DATABASE_PORT: int = 5432
    DATABASE_HOST: str = "localhost"
    # Admin
    ADMIN_USER: str = "admin"
    ADMIN_PASS: str = "admin"
    ADMIN_EMAIL: EmailStr = "admin@admin.com"
    # SMTP
    MAIL_USERNAME: str = "test_mail_username"
    MAIL_PASSWORD: str = "test_mail_password"
    MAIL_FROM: str = ""
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "test_mail_server"
    MAIL_FROM_NAME: str = "KebabEstate"
    TEST_SEND_EMAIL: bool = False
    TEST_TARGET_EMAIL: str | None = ""

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=(
            "project.env",
            ".env",
        ),
    )

    @computed_field(return_type=str)
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"  # noqa

    @computed_field(return_type=str)
    def TEST_DATABASE_URL(self):
        # sqlite with async
        return "sqlite+aiosqlite:///./test.db"

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
